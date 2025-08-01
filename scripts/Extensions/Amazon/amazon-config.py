#!/usr/bin/env python
import amazon
import json
import argparse

import GameSet


class AmazonArgs(GameSet.GenericArgs):
    def __init__(self, setNameConfig):
        super().__init__()
        self.addArguments()
        self.setNameConfig = setNameConfig

    def addArguments(self):
        super().addArguments()
        self.parser.add_argument(
            '--list', help='Get list of amazon games', action='store_true')
        self.parser.add_argument(
            '--get-game-dir', help='Get install directory for game')
        self.parser.add_argument(
            '--getprogress', help='Get installation progress for game')
        self.parser.add_argument(
            '--get-proton', help='Get proton command')
        self.parser.add_argument(
            '--get-args', help='Get game arguments')
        self.parser.add_argument(
            '--launchoptions', nargs=3, help='Get launch options')
        self.parser.add_argument(
            '--getloginstatus', help='Get login status', action='store_true')
        self.parser.add_argument(
            '--get-base64-images', help='Get base64 images for short name')
        self.parser.add_argument(
            '--offline', help='Offline mode', action='store_true')
        self.parser.add_argument(
            '--update-game-details', help='Update game details')
        self.parser.add_argument(
            '--flush-cache', help='Flush cache', action='store_true')
        self.parser.add_argument(
            '--add-missing-details', help='Update games with missing details', action='store_true')
        self.parser.add_argument(
            '--process-info-file', help='Process info file')
        self.parser.add_argument(
            '--import-info-file', help='Import info file into DB')
        self.parser.add_argument(
            '--get-game-size', help='Get game size')
        self.parser.add_argument(
            '--gen-install-deps', nargs=2, help='Generate install dependencies for game')

    def parseArgs(self):
        super().parseArgs()
        self.gameSet = amazon.Amazon(self.args.dbfile, storeName="Amazon", setNameConfig=self.setNameConfig)
        self.gameSet.create_tables()

    def processArgs(self):
        try:
            super().processArgs()

            if self.args.list:
                print(self.gameSet.get_list(self.args.offline))
            if self.args.get_game_dir:
                print(self.gameSet.get_game_dir(self.args.get_game_dir, self.args.offline))
            if self.args.getprogress:
                print(self.gameSet.get_last_progress_update(self.args.getprogress))
            if self.args.get_proton:
                print(self.gameSet.get_proton_command(self.args.get_proton))
            if self.args.get_args:
                print(self.gameSet.get_parameters(self.args.get_args, self.args.offline))
            if self.args.launchoptions:
                print(self.gameSet.get_launch_options(
                    self.args.launchoptions[0],
                    self.args.launchoptions[1],
                    self.args.launchoptions[2],
                    self.args.offline
                ))
            if self.args.getloginstatus:
                print(self.gameSet.get_login_status(self.args.offline, getattr(self.args, "flush_cache", False)))
            if self.args.get_base64_images:
                print(self.gameSet.get_base64_images(self.args.get_base64_images))
            if self.args.update_game_details:
                self.gameSet.update_game_details(self.args.update_game_details, self.args.offline)
            if self.args.add_missing_details:
                self.gameSet.add_missing_info()
            if self.args.process_info_file:
                self.gameSet.process_info_file(self.args.process_info_file)
            if self.args.import_info_file:
                self.gameSet.import_info_file(self.args.import_info_file)
            if self.args.get_game_size:
                print(self.gameSet.get_game_size(self.args.get_game_size, self.args.offline))
            if self.args.gen_install_deps:
                print(self.gameSet.gen_install_deps(self.args.gen_install_deps[0], self.args.gen_install_deps[1]))

            if not any(vars(self.args).values()):
                self.parser.print_help()
        except amazon.CmdException as e:
            print(json.dumps({'Type': 'Error', 'Content': {'Message': e.args[0]}}))


def main():
    amazonArgs = AmazonArgs(setNameConfig="Proton")
    amazonArgs.parseArgs()
    amazonArgs.processArgs()


if __name__ == '__main__':
    main()
