from auth.utils import generate_token, verify_token

sample_email = "muhdhammad@gmail.com"

token = generate_token(email=sample_email)
print(token)

verify = verify_token(token=token)
print(verify)


