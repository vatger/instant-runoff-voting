from limesurvey import Limesurvey
from vatger_db import VatgerDB


def map_db_user_to_obj(o):
    return {
        "email": o[2],
        "firstname": "member",
        "lastname": o[1]
    }


if __name__ == '__main__':
    limesurvey = Limesurvey()
    vdb = VatgerDB()

    survey_name = input("Enter Survey-Name (this will be displayed in the dashboard): ")
    forum_group = input("Enter Forum-Group ID: ")
    survey_id = input("Enter Survey-ID: ")
    valid_till = input("Enter valid-until date (optional - YYYY-MM-DD HH:mm:ss in UTC): ")

    truncate_prompt = input("\nDo you want to truncate the survey_keys Table? [y/n]")
    if truncate_prompt == 'y':
        vdb.truncate_survey_keys()
        print("Table truncated.")

    user_arr = []
    r = vdb.get_members_from_forum_group(int(forum_group))
    for res in r:
        user_arr.append(map_db_user_to_obj(res))

    print("\n\n================= Review Selection =================\n"
          f"Survey Name: {survey_name}\n"
          f"Forum-Group-ID: {int(forum_group)}\n"
          f"Survey-ID: {int(survey_id)}\n"
          f"\n"
          f"Received {len(r)} members.\n"
          f"Parsed {len(user_arr)} members.\n"
          f"\n"
          f"Do you wish to add these to the survey?\n")

    prompt = input('[y/n/p(rint)] ')
    while True:
        if prompt == 'p':
            for u in user_arr:
                print(f"{u['lastname']} - {u['email']}")
        elif prompt == 'n':
            exit(0)
        elif prompt == 'y':
            break

        prompt = input('[y/n/p(rint)] ')

    participants = limesurvey.add_participants(int(survey_id), user_arr)
    participant_list = []
    for p in participants:
        participant_list.append((int(p['lastname']),
                                 survey_name,
                                 p['token'],
                                 f"https://survey.vatsim-germany.org/index.php?r=survey/index&token={p['token']}&sid={int(survey_id)}&lang=de-informal",
                                 valid_till if (valid_till != '') else 'NULL')
                                )

    prompt = input("Do you want to review the user list one last time? [n/q(uit)/p(rint)")
    while True:
        if prompt == 'p':
            for p in participant_list:
                print(f"{p[0]} - {p[2]} (Survey: {p[1]})")
        elif prompt == 'q':
            exit(0)
        elif prompt == 'n':
            break

        prompt = input('[n/q(uit)/p(rint) ')

    print("Adding survey Keys...")
    vdb.add_survey_keys(participant_list)
    print(f"Done. {len(participant_list)} keys added. Do you want to activate the survey now?")
    activate_prompt = input("[y/n] ")

    if activate_prompt == 'y':
        limesurvey.activate_survey(int(survey_id))
        print("Done")