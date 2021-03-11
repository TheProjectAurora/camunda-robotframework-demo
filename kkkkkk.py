import owncloud

oc = owncloud.Client("http://localhost:80")
x = oc.login('sakke','sakke')
print(x)
oc.put_file('remotefile.txt', 'localfile.txt')
link_info = oc.share_file_with_link('remotefile.txt')
print ("Here is your link: " + link_info.get_link())