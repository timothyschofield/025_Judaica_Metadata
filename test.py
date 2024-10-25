from helper_functions_judaica import decimal_encode_for_xml



test = "ajsd&#x27;kajüsd"
test = ""

output = test.replace("&#x27;","'")


#output = decimal_encode_for_xml(test)

print(f"****{output}****")


