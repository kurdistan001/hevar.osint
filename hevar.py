import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import random


init(autoreset=True)


BANNER = f"""
{Fore.RED}█████                                              
{Fore.RED}░░███                                               
{Fore.RED} ░███████    ██████  █████ █████  ██████   ████████ 
{Fore.RED} ░███░░███  ███░░███░░███ ░░███  ░░░░░███ ░░███░░███
{Fore.RED} ░███ ░███ ░███████  ░███  ░███   ███████  ░███ ░░░ 
{Fore.RED} ░███ ░███ ░███░░░   ░░███ ███   ███░░███  ░███     
{Fore.RED} ████ █████░░██████   ░░█████   ░░████████ █████    
{Fore.RED}░░░░ ░░░░░  ░░░░░░     ░░░░░     ░░░░░░░░ ░░░░░     
{Fore.RED}╔══════════════════════════════════╗
{Fore.RED}║    HEVAR OSINT SCANNER v3.0      ║
{Fore.RED}║        bzhi kurdistan            ║
{Fore.RED}╚══════════════════════════════════╝
"""


LOADING_MSGS = [
    "tawaw bw 🔥...",
    "tawaw bw 🔥...",
    "tawaw bw 🔥...",
    "tawaw bw 🔥...",
    "tawaw bw 🔥...",
    "tawaw bw 🔥...",
    "tawaw bw 🔥..."
]

FUN_FACTS = {
    "ba bashi toolaka bakar bena",
    "Pro tip: Always get permission before scanning!",
    "Remember: With great power comes great responsibility!",
}

PLATFORMS = {
    
    "Facebook": "https://www.facebook.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Pinterest": "https://pinterest.com/{}",
    "Reddit": "https://reddit.com/user/{}",
    "LinkedIn": "https://linkedin.com/in/{}",
    "YouTube": "https://youtube.com/{}",
    "Twitch": "https://twitch.tv/{}",
    "VK": "https://vk.com/{}",
    "Weibo": "https://weibo.com/{}",
    "QQ": "https://qzone.qq.com/{}",
    "Badoo": "https://badoo.com/{}",
    "Meetup": "https://meetup.com/{}",
    "Nextdoor": "https://nextdoor.com/{}",
    "Tagged": "https://tagged.com/{}",
    "Hi5": "https://hi5.com/{}",
    "Bumble": "https://bumble.com/{}",
    "Grindr": "https://grindr.com/{}",
    "Tinder": "https://tinder.com/{}",
    "Flickr": "https://flickr.com/people/{}",
    "Vero": "https://vero.co/{}",
    "Mastodon": "https://mastodon.social/@{}",
    "Ello": "https://ello.co/{}",
    "Rumble": "https://rumble.com/user/{}",
    "Dailymotion": "https://dailymotion.com/{}",
    "Likee": "https://likee.com/@{}",
    "Triller": "https://triller.co/@{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Discord": "https://discord.com/users/{}",
    "Telegram": "https://t.me/{}",
    "Signal": "https://signal.me/#{}",
    "Line": "https://line.me/ti/p/{}",
    "Kik": "https://kik.me/{}",
    "Skype": "https://join.skype.com/{}",
    "WhatsApp": "https://wa.me/{}",
    "Viber": "https://chats.viber.com/{}",
    "WeChat": "https://wechat.com/{}",
    "Clubhouse": "https://clubhouse.com/@{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Mixcloud": "https://mixcloud.com/{}",
    "ReverbNation": "https://reverbnation.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Blogger": "https://{}.blogspot.com",
    "WordPress": "https://{}.wordpress.com",

 
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "StackExchange": "https://stackexchange.com/users/{}",
    "Dev.to": "https://dev.to/{}",
    "CodePen": "https://codepen.io/{}",
    "CodeSandbox": "https://codesandbox.io/u/{}",
    "Replit": "https://replit.com/@{}",
    "Kaggle": "https://kaggle.com/{}",
    "HackerRank": "https://hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}",
    "Codewars": "https://codewars.com/users/{}",
    "Topcoder": "https://topcoder.com/members/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://behance.net/{}",
    "Figma": "https://figma.com/@{}",
    "Adobe": "https://profile.adobe.com/{}",
    "Canva": "https://canva.com/{}",
    "ProductHunt": "https://producthunt.com/@{}",
    "AngelList": "https://angel.co/{}",
    "Crunchbase": "https://crunchbase.com/person/{}",
    "SlideShare": "https://slideshare.net/{}",
    "SpeakerDeck": "https://speakerdeck.com/{}",
    "Notion": "https://notion.so/{}",
    "Airtable": "https://airtable.com/{}",
    "Trello": "https://trello.com/{}",
    "Asana": "https://app.asana.com/{}",
    "Jira": "https://{}.atlassian.net",
    "Slack": "https://{}.slack.com",
    "GooglePlay": "https://play.google.com/store/apps/dev?id={}",
    "AppStore": "https://apps.apple.com/us/developer/{}",
    "Microsoft": "https://microsoft.com/en-us/us/{}",
    "IBM": "https://ibm.com/developerworks/community/{}",
    "Oracle": "https://community.oracle.com/{}",
    "Salesforce": "https://trailblazer.me/id/{}",
    "SAP": "https://people.sap.com/{}",
    "Coursera": "https://coursera.org/user/{}",
    "Udemy": "https://udemy.com/user/{}",
    "edX": "https://edx.org/user/{}",
    "KhanAcademy": "https://khanacademy.org/profile/{}",
    "Duolingo": "https://duolingo.com/profile/{}",
    "ResearchGate": "https://researchgate.net/profile/{}",
    "Academia": "https://independent.academia.edu/{}",
    "GoogleScholar": "https://scholar.google.com/citations?user={}",
    "ORCID": "https://orcid.org/{}",
    "IEEE": "https://ieee.org/membership/profile/{}.html",
    "ACM": "https://dl.acm.org/profile/{}",
    "arXiv": "https://arxiv.org/user/{}",

    
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "IMDb": "https://imdb.com/user/{}",
    "Goodreads": "https://goodreads.com/{}",
    "Letterboxd": "https://letterboxd.com/{}",
    "DeviantArt": "https://{}.deviantart.com",
    "ArtStation": "https://artstation.com/{}",
    "Pixiv": "https://pixiv.net/users/{}",
    "Newgrounds": "https://{}.newgrounds.com",
    "Fandom": "https://fandom.com/u/{}",
    "Instructables": "https://instructables.com/member/{}",
    "Hackaday": "https://hackaday.io/{}",
    "Thingiverse": "https://thingiverse.com/{}",
    "MyMiniFactory": "https://myminifactory.com/users/{}",
    "Gumroad": "https://gumroad.com/{}",
    "Patreon": "https://patreon.com/{}",
    "BuyMeACoffee": "https://buymeacoffee.com/{}",
    "Ko-fi": "https://ko-fi.com/{}",
    "Substack": "https://{}.substack.com",
    "Ghost": "https://{}.ghost.io",
    "Medium": "https://medium.com/@{}",
    "Blogspot": "https://{}.blogspot.com",
    "WordPress": "https://{}.wordpress.com",
    "Wix": "https://{}.wix.com",
    "Squarespace": "https://{}.squarespace.com",
    "Webflow": "https://{}.webflow.io",
    "Shopify": "https://{}.myshopify.com",
    "Etsy": "https://etsy.com/shop/{}",
    "eBay": "https://ebay.com/usr/{}",
    "Amazon": "https://amazon.com/gp/profile/amzn1.account.{}",
    "AliExpress": "https://aliexpress.com/store/{}",
    "Booking": "https://booking.com/profile/{}",
    "Airbnb": "https://airbnb.com/users/show/{}",
    "TripAdvisor": "https://tripadvisor.com/Profile/{}",
    "Yelp": "https://yelp.com/user_details?userid={}",
    "Foursquare": "https://foursquare.com/user/{}",
    "Zillow": "https://zillow.com/profile/{}",
    "Realtor": "https://realtor.com/realestateagents/{}",
    "Indeed": "https://indeed.com/profile/{}",
    "Glassdoor": "https://glassdoor.com/member/profile/{}",
    "Monster": "https://monster.com/profile/{}",
    "CareerBuilder": "https://careerbuilder.com/profile/{}",
    "Upwork": "https://upwork.com/freelancers/{}",
    "Fiverr": "https://fiverr.com/{}",
    "Freelancer": "https://freelancer.com/u/{}",
    "Toptal": "https://toptal.com/resume/{}",
    "99designs": "https://99designs.com/profiles/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://behance.net/{}"
}

def print_banner():
    print(BANNER)
    print(f"{Fore.RED}📸 la Snapchat addm kan: {Fore.WHITE}@hevar.hersh1")
    print(f"{Fore.RED}🔥 Bzhi Kurd! Bzhi Kurdistan! 🔥")
    print(f"\n{Fore.WHITE}🔍 Scanning dast pedaka")
    print(f"{Fore.WHITE}🚀 bashtren username scanner")

def check_platform(username, platform, url):
    try:
        response = requests.get(
            url.format(username),
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
            allow_redirects=False
        )
        
        if response.status_code == 200:
            return (platform, True, url.format(username))
        return (platform, False, None)
    except:
        return (platform, False, None)

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.RED}⏳ scan dast pedaka {i} seconds...", end='\r')
        time.sleep(1)
    print(" " * 50, end='\r')  # Clear line

def run_scan(username):
    print_banner()
    print(f"{Fore.CYAN}🚀 scanning bo: {Fore.YELLOW}{username}{Fore.RESET}")
    
    # 30-second waiting session
    print(f"\n{Fore.RED}⚠ scan daste pekrd...")
    countdown_timer(5)
    
    print(f"\n{Fore.WHITE}{random.choice(LOADING_MSGS)}\n")
    
    start_time = time.time()
    found_count = 0
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(check_platform, username, platform, url)
            for platform, url in PLATFORMS.items()
        ]
        
        for i, future in enumerate(as_completed(futures)):
            platform, exists, url = future.result()
            if exists:
                print(f"{Fore.GREEN}✅ {platform.ljust(20)}: dozrawa {url}")
                found_count += 1
            else:
                print(f"{Fore.RED}❌ {platform.ljust(20)}: nadozrawa")
            
            if (i+1) % 10 == 0:
                print(f"{Fore.WHITE}▷ Progress: {i+1}/150 ({round((i+1)/150*100)}%)")
    
    print(f"\n{Fore.CYAN}🎉 Scan tawaw bw in {time.time()-start_time:.2f} seconds")
    print(f"{Fore.GREEN}✔ dozrawa {found_count} matches")
    print(f"{Fore.RED}✖ {150-found_count} platforms nadozrawa")
    print(f"\n{Fore.RED}🔥 Bzhi Kurd! Bzhi Kurdistan! 🔥")
    print(f"{Fore.RED}📸 la snapchat addm kan: {Fore.WHITE}@hevar.hersh1")



if __name__ == "__main__":
    username = input(f"{Fore.YELLOW}username dane bo scan: {Fore.WHITE}")
    run_scan(username)
