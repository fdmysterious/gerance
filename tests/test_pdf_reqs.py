from gerance.pdf import requirement_file

reqs = requirement_file.parse(
    "test_requirements.pdf",
    r"\[(?P<req_id>REQ-[0-9]{4})-(?P<req_version>[A-Z])\]\s*(?P<req_name>.*?)$"
)

print(reqs)
