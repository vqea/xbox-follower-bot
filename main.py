import asyncio
import aiohttp
from colorama import init
from sys import platform
from os import system, _exit


class Follow_Bot:
    def __init__(self):
        self.users = self.collect_tokens()
        self.followed = 0
        self.failed = 0
        self.target = ''


    async def follow_target(self, token) -> None:
        session = aiohttp.ClientSession()

        async with session.put(f'https://social.xboxlive.com/users/me/people/gt({self.target})', headers={ "Authorization": token, "X-XBL-Contract-Version": "2" }) as follow_request:
            if follow_request.status in [200, 201, 202, 204]: 
                self.followed += 1 

            else:
                self.failed += 1             

            print(f" [\x1b[1;32m+\x1b[1;37m] target: ({self.target}) | followed: ({self.followed}) | failed: ({self.failed})", end='\r', flush=True)
        await session.close()   
 

    @staticmethod
    def collect_tokens() -> None:
        with open('tokens/tokens.txt', 'r') as token_file:
            return [token.strip() for token in token_file]

    
    async def initialise(self) -> None:
        system('cls' if platform == 'win32' else 'clear')
        init(autoreset=True)
        print(' [\x1b[1;32m*\x1b[39m] slya\'s xbox follower bot')

        if len(open('tokens/tokens.txt', 'r').readlines()) > 0:
            print(f" [\x1b[1;32m*\x1b[39m] Tokens: ({len(open('tokens/tokens.txt', 'r').readlines())}) \n")
        else:
            print(' [\x1b[1;31m!\x1b[39m] no tokens found in \'\x1b[1;33mtokens/tokens.txt\x1b[39m\'');_exit(0)

        self.target = input(' [\x1b[1;32m?\x1b[39m] target: ');print('')
        await self.start()


    async def start(self):
        await asyncio.gather(*[self.follow_target(user) for user in self.users])
        print(f" [\x1b[1;32m+\x1b[1;37m] target: ({self.target}) | followed: ({self.followed}) | failed: ({self.failed})", flush=True)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(Follow_Bot().initialise())
