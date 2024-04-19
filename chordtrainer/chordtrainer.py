import yaml

with open('D:\\git-repo\\projects\\chordtrainer\\build2.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)
    print(prime_service['song'])