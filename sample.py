with open("/home/runner/.ssh/id_rsa.pub") as f:
    with open("./ssh.txt", mode='w') as s:
        s.write(f.read())