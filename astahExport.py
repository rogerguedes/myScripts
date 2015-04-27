import re
import sys
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["class="])
except getopt.GetoptError:
    print "voce precisa especificar qual arquivo contem as classes."
    sys.exit(2)
myFile = []
try:
    myFile = open(args[0], "r");
except IOError as e:
    print e
except IndexError as e:
    print "voce precisa especificar qual arquivo contem as classes."

classes = {}
for line in myFile:
    result = re.search(r'"([\w\s:]*)","([\w\s:]*)","([\w\s:]*)"', line);
    if result:
        #get current class sign
        classe = {}
        classe["fullSign"] = result.group(2)
        #get current attr sign
        attr = {}
        attr["fullSign"] = result.group(1)
        
        result = re.search(r'(\w*)$', classe["fullSign"]);
        classe["name"] = result.group(1)
        if not classes.has_key(classe["name"]):
            classes[classe["name"]] = []
        result = re.search(r'(\w*)[\s:]*(\w*)[\s:]*(\w*)', attr["fullSign"]);
        attr["visibility"] = result.group(1)
        attr["name"] = result.group(2)
        attr["type"] = result.group(3)
        classes[classe["name"]].append({"visibility": attr["visibility"], "name": attr["name"], "type": attr["type"]})
if len(classes) == 0:
    print "voce nao possui classes nesse arquivo"
tabs = "    "
myFile.close()

for classeDaVez in classes.keys():
    try:
        myFile = open(classeDaVez.lower()+".php", "w");
    except IOError as e:
        print e
    myFile.write("<?php\n")
    myFile.write("class "+classeDaVez+"{\n")
    for atrib in classes[classeDaVez]:
        myFile.write(tabs+atrib["visibility"]+" "+"$"+atrib["name"]+";\n")
    myFile.write(tabs+"\n")
    myFile.write(tabs+"public function __construct(")
    quantParams = len(classes[classeDaVez])
    i = 0
    for i in range(quantParams - 1):
        myFile.write("$param"+str(i)+", ")
    myFile.write("$param"+str(i+1)+"){\n")
    for i in range(quantParams):
        myFile.write(str(tabs+tabs+"$this->%s = %s" % (str(classes[classeDaVez][i]["name"]), "$param"+str(i)+";\n")))
    myFile.write(tabs+"}\n")
    myFile.write("}\n")
    myFile.write("?>\n")
    myFile.close()

