year = '      		  	 \n' + '	\n' + '      		    \n' + '	\n' + \
    '      		  	 \n' + '	\n' + '      		    \n' + '	\n' + '  \n' + '\n' + '\n'
print("year = ")
for x in year:
    if x == '	':
        print(1, end="")
    elif x == ' ':
        print(0, end="")
    elif x == '\n':
        print()
