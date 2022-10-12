import json
from utils import utils

def generate(
    input: str
):
    '''
    List of commands to be added:
        - payloads
        - use
        - generate
        - generate <payload>
    '''

    if type(input) == list:
        input = ''.join(input)

    data = input.lower().split('/')

    with open('agents/agents.json', 'r') as f:
        agents = json.load(f)

    agents = [agent.lower() for agent in agents]

    if data[0] not in agents:
        utils.log_error(f"Invalid agent: {data[0]}")
        return None

    