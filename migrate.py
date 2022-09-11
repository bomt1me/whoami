import argparse

import migrations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform whoami migration.")
    parser.add_argument("migration", type=str, help="Migrate up or down.", choices=["up", "down"])
    args = parser.parse_args()
    if args.migration == "down":
        migrations.down()
    else:
        migrations.up()
