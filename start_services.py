import subprocess
from config import config
from argparse import ArgumentParser

def start_service(args, config, n):
    service = "facade" if args.facade else "logging" if args.logging else "message"
    if isinstance(config[service], list):
        host = config[service][n][7:16]
        port = config[service][n][-4:]
    else:
        host = config[service][7:16]
        port = config[service][-4:]
    subprocess.run(f"python {service}_service.py {host} {port}", shell=True)

if __name__ == "__main__":
    parser = ArgumentParser(prog='start_service.py')
    parser.add_argument("--facade", action="store_const", const=True)
    parser.add_argument("--logging", action="store_const", const=True)
    parser.add_argument("--message", action="store_const", const=True)
    parser.add_argument("--number", "-n", type=int, required=False, default=0)
    args = parser.parse_args()

    # Start Consul
    subprocess.run("consul agent -dev", shell=True)

    # Start the specified service
    start_service(args, config, args.number)
