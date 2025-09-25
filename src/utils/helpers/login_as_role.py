from src.utils.helpers.login_helper import login_with_credentials


# async def login_as_role(page, role: str):
#     user_data = get_random_credentials_from_google_sheet(role)
#
#     await login_with_credentials(
#         page,
#         role=role,
#         email=user_data["email"],
#         password=user_data["password"]
#     )
#
#     return user_data
