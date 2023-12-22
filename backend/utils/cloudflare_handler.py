async def cloudflare_decode_email(string):
    r = int(string[:2], 16)
    email = "".join(
        [chr(int(string[i : i + 2], 16) ^ r) for i in range(2, len(string), 2)]
    )
    return email
