import argparse

parser = argparse.ArgumentParser(prog="Raidware", description='Raidware - A C2 Framework.')
subparsers = parser.add_subparsers(dest='subparser_name')

server_parser = subparsers.add_parser('server', help='Start the Raidware Teamserver.')
server_parser.add_argument('-H', '--host', help='Specify the host to bind the Teamserver to.', default='0.0.0.0', type=str)
server_parser.add_argument('-p', '--port', help='Specify the port to bind the Teamserver to.', default=5000, type=int)
server_parser.add_argument('-d', '--debug', help='Enable debug mode.', action='store_true')
server_parser.add_argument('-T', '--team-password', help='Set a custom Team Password that your team will authenticate with', default=None, type=str)

cli_parser = subparsers.add_parser('cli', help='Start the Raidware CLI.')
cli_parser.add_argument('-H', '--host', help='Specify the host of the Teamserver.', default='127.0.0.1', type=str)
cli_parser.add_argument('-p', '--port', help='Specify the port of the Teamserver.', default=5000, type=int)
cli_parser.add_argument('-U', '--username', help='Specify the username you specified when registering.', required=True, type=str)
cli_parser.add_argument('-P', '--password', help='Specify the password you specified when registering.', required=True, type=str)
cli_parser.add_argument('-T', '--team-password', help="Specify the team's password that was given to you when you ran Raidware.", required=True, type=str)

args = parser.parse_args()

if args.subparser_name == 'cli':
    ''' All CLI Parsing '''
    host = args.host
    port = args.port
    username = args.username
    password = args.password
    team_password = args.team_password

    print("Unimplemented. Will be working on it soon...")
    print(f"\nHost: {host}")
    print(f"Port: {port}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Team Password: {team_password}")
    print("\nRegards,\nTeam Raidware!")

elif args.subparser_name == 'server':
    ''' All Server Parsing '''
    host = args.host
    port = args.port
    debug = args.debug
    team_password = args.team_password

    from Teamserver.app import init
    init(host = host, port = port, debug = debug, team_pass=team_password)