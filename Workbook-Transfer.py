###################################################################################################################################
#This program will be unable to publish a workbook that contains two data sources with two different sets of  embedded credentials.
###################################################################################################################################

import os
from tableaudocumentapi import Workbook
from tableaudocumentapi import Datasource

#################################Old Server#################################
old_server = "Server Name"
old_site = "Site Name"
workbook = "\"Workbook Name\""
old_username = ""
old_password = ""
############################################################################

################################New Server##################################
new_server = "Server Name"
new_site = "Site Name"
new_project = "Project Name"
new_username = ""
new_password = ""
############################################################################

filetype = ".twbx"
output_file_path = "./Viz/"

if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)

name_nospace = ""
for x in workbook:
	if x!= "\"" and x!= " " and x!= "(" and x!= ")":
		name_nospace+="".join(x)

name_noquotes = ""
for x in workbook:
	if x!= "\"":
		name_noquotes+="".join(x)

if old_site == "Default":
	old_site = '""'

if new_site == "Default":
	new_site = '""'

############################Old Server Commandline##########################
old_login = "tabcmd login -s " + old_server + " -t " + old_site + " -u " + old_username + " -p " +old_password
old_URL = "/workbooks/"+name_nospace+filetype
get_command = "tabcmd get " +old_URL+ " -f " +output_file_path+workbook+filetype
############################################################################
os.system(old_login)
os.system(get_command)

#print output_file_path+name_noquotes
sourceWB = Workbook(output_file_path+name_noquotes+filetype)

############################New Server Commandline##########################
new_login = "tabcmd login -s " + new_server + " -t " + new_site + " -u " +new_username + " -p " +new_password
message = "It appears you have a live datasource. Please enter the password for "
logout = "tabcmd logout"
############################################################################
db_user = ""
db_pass = ""

for x in sourceWB.datasources:	
	if x.name.startswith ("sqlproxy") or x.name.startswith("federated"):
		for j in x.connections:
			if j.dbclass != "textscan" and j.dbclass != "excel-direct" and not (j.dbclass == "msaccess" and j.authentication=="no"):
				if x.name.startswith("sqlproxy"):
					os.system ("tabcmd get datasources/"+j.dbname + ".tdsx -f " + output_file_path+j.dbname +".tdsx")
					os.system(new_login)
					os.system ("tabcmd publish " + output_file_path+j.dbname + ".tdsx -n " +j.dbname)
					os.remove(output_file_path+j.dbname +".tdsx")
					os.system(old_login)
				else:
					db_user = j.username
					db_pass = raw_input(message + j.dbname +": ")
					db_pass

os.system(new_login)
publish = "tabcmd publish \"" + output_file_path + name_noquotes + filetype + "\" --project \"" + new_project + "\" -n \"" + name_noquotes + "\" --db-username \"" +db_user + "\" --db-password \"" + db_pass + "\" -o"
os.system (publish)
os.remove (output_file_path + name_noquotes + filetype)
os.rmdir (output_file_path)
os.system (logout)