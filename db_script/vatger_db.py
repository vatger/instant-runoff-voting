from sql_connector import SqlConnector


class VatgerDB:
    def __init__(self):
        self.sql_conn = SqlConnector()

    def truncate_survey_keys(self):
        self.sql_conn.execute(
            "TRUNCATE TABLE survey_keys",
            "hp"
        )

    def get_survey_keys(self):
        res = self.sql_conn.execute_select(
            "SELECT * FROM survey_keys",
            "hp"
        )
        return res

    def add_survey_keys_with_date(self, s_keys):
        self.sql_conn.execute(
            f"INSERT INTO survey_keys (account_id, name, token, url, valid_till) VALUES {str(s_keys).strip('[]')}",
            "hp"
        )

    def add_survey_keys_without_date(self, s_keys):
        self.sql_conn.execute(
            f"INSERT INTO survey_keys (account_id, name, token, url) VALUES {str(s_keys).strip('[]')}",
            "hp"
        )

    def get_members_from_forum_group(self, forum_group_id: int):
        res = self.sql_conn.execute_select(
            f"select 'member', custom_title, email from xf_user inner join xf_user_group_relation on xf_user.user_id = xf_user_group_relation.user_id where xf_user_group_relation.user_group_id  = {forum_group_id}",
            "board"
        )
        return res
