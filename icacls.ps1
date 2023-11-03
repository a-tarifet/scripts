
# Creates temp folder
mkdir  C:\temp

#Export the current ICACLS
icacls C:\ > C:\temp\exportedicals.txt

#Remove the users group
icacls C:\ /remove "BUILTIN\Users"


