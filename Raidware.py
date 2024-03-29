import argparse

banner = "Raidware - A C2 Framework."
def version():
    with open('version.conf', 'r') as f:
        version = f.read()
    return f"{banner.split()[0]} v{version.split()[0]}"

parser = argparse.ArgumentParser(prog="Raidware", description=banner)
parser.add_argument('-v', '--version', help='Print the version of Raidware.', dest='version', action='version', version=version())
subparsers = parser.add_subparsers(required=True, dest='mode')

server_parser = subparsers.add_parser('server', help='Start the Raidware Teamserver.')
server_parser.add_argument('-H', '--host', help='Specify the host to bind the Teamserver to.', default='0.0.0.0', type=str)
server_parser.add_argument('-p', '--port', help='Specify the port to bind the Teamserver to.', default=5000, type=int)
server_parser.add_argument('-D', '--debug', help='Enable debug mode.', action='store_true')
server_parser.add_argument('-T', '--team-password', help='Set a custom Team Password that your team will authenticate with', default=None, type=str)
server_parser.add_argument('-B', '--background', help="Run the Teamserver in the background.", action='store_true')
server_parser.add_argument('--https', help='Use HTTPS communication.', action='store_true', default=False)

cli_parser = subparsers.add_parser('cli', help='Start the Raidware CLI.')
cli_parser.add_argument('-H', '--host', help='Specify the host of the Teamserver.', type=str, required=True)
cli_parser.add_argument('-p', '--port', help='Specify the port of the Teamserver.', type=int, required=True)
cli_parser.add_argument('-U', '--username', help='Specify the username you specified when registering.', required=True, type=str)
cli_parser.add_argument('-P', '--password', help='Specify the password you specified when registering.', required=True, type=str)
cli_parser.add_argument('-T', '--team-password', help="Specify the team's password that was given to you when you ran Raidware.", required=True, type=str)
cli_parser.add_argument('--https', help='Use HTTPS to connect to the Teamserver.', action='store_true', default=False)

args = parser.parse_args()

if args.mode == 'cli':
    from CLI.cli import init
    init(host=args.host, port=args.port, username=args.username, password=args.password, team_password=args.team_password, https=args.https)

elif args.mode == 'server':
    if args.background:
        print("Background mode isn't currently available. Will update it soon.")

    from Teamserver.app import init
    init(host=args.host, port=args.port, debug=args.debug, team_pass=args.team_password, https=args.https)
