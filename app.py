import os
import sys
import subprocess


G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
R = '\033[91m'  # Red
C = '\033[96m'  # Cyan
B = '\033[1m'   # Bold
W = '\033[0m'   # Reset

def clear_screen():
    os.system('clear')

def print_banner():
    print(f"{C}{B}")
    print("""
███████╗ █████╗ ██╗   ██╗███████╗     █████╗ ███╗   ██╗██╗   ██╗    
██╔════╝██╔══██╗██║   ██║██╔════╝    ██╔══██╗████╗  ██║╚██╗ ██╔╝    
███████╗███████║██║   ██║█████╗      ███████║██╔██╗ ██║ ╚████╔╝     
╚════██║██╔══██║╚██╗ ██╔╝██╔══╝      ██╔══██║██║╚██╗██║  ╚██╔╝      
███████║██║  ██║ ╚████╔╝ ███████╗    ██║  ██║██║ ╚████║   ██║       
╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       
                                                                    
██╗   ██╗██╗██████╗ ███████╗ ██████╗                                
██║   ██║██║██╔══██╗██╔════╝██╔═══██╗                               
██║   ██║██║██║  ██║█████╗  ██║   ██║                               
╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║                               
 ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝                               
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝                                
 Instagram  ❤️ @cyber_raj1 | Telegram  @cyber_raj1 3000 plus websites video download easly ❤️
    """)
    print(f"{W}")


DOWNLOAD_DIR = "D:\\youtube"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def setup_and_update():
    """Checks for updates and ensures yt-dlp is latest"""
    print(f"{Y}🔄 Checking for updates & setting up...{W}")
    
    subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{G}✓ System is Up-to-date!{W}\n")

def download_engine():
    url = input(f"\n{B}{C}🔗 Paste Video/Reel/Post URL: {W}").strip()
    if not url:
        print(f"{R}Error: URL khali hai!{W}")
        return

    print(f"\n{Y}📡 Fetching details from {url.split('/')[2]}...{W}")
    
    
    os.system(f'python -m yt_dlp -F"{url}"')
    
    print(f"\n{B}{Y}--- Quality & Format Options ---{W}")
    print(f"{G}1.{W} Video: Best Quality (Auto)")
    print(f"{G}2.{W} Video: 720p (HD)")
    print(f"{G}3.{W} Video: 480p (SD)")
    print(f"{G}4.{W} Audio: Only MP3")
    print(f"{G}5.{W} Manual: Enter Format Code")
    
    choice = input(f"\n{B}Select (1-5): {W}").strip()
    
    
    cmd_opts = f'--no-mtime --embed-thumbnail -o "{DOWNLOAD_DIR}%(title)s.%(ext)s"'
    
    if choice == "1":
        f_str = "bestvideo+bestaudio/best"
    elif choice == "2":
        f_str = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif choice == "3":
        f_str = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    elif choice == "4":
        f_str = "bestaudio/best"
        cmd_opts += " -x --audio-format mp3"
    elif choice == "5":
        fid = input(f"{Y}Enter Format ID: {W}").strip()
        f_str = fid
    else:
        f_str = "best"

    print(f"\n{B}{G}📥 Downloading... (Please wait){W}\n")
    
    # Final command execution
    final_cmd = f'python -m yt_dlp {cmd_opts} -f "{f_str}" "{url}"'
    status = os.system(final_cmd)
    
    if status == 0:
        print(f"\n{G}✅ SUCCESS: File saved in Download folder!{W}")
    else:
        print(f"\n{R}❌ ERROR: Download failed. Check link or try another quality.{W}")

def main():
    clear_screen()
    print_banner()
    setup_and_update()
    
    while True:
        print(f"\n{C}{'━'*40}{W}")
        print(f"{B}  MULTI-SITE VIDEO DOWNLOADER {W}")
        print(f"{C}{'━'*40}{W}")
        print(f"{G}[1]{W} Start Download (FB, IG, YT, etc.)")
        print(f"{G}[2]{W} Open Download Folder")
        print(f"{G}[3]{W} Exit")
        
        choice = input(f"\n{B}Choice: {W}").strip()
        
        if choice == "1":
            download_engine()
        elif choice == "2":
            print(f"\n{Y}📂 Files in {DOWNLOAD_DIR}:{W}")
            os.system(f'ls -p "{DOWNLOAD_DIR}" | grep -v /')
            input(f"\n{C}Press Enter to go back...{W}")
        elif choice == "3":
            print(f"\n{R}👋 Jai shree Raam {W}")
            break
        else:
            print(f"{R}Invalid Choice!{W}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}🛑 Script Stopped.{W}")
        sys.exit()
