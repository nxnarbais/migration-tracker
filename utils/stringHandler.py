def isMatchingRegex(stringToMatch, rgx):
  if (type(stringToMatch) is str):
    if (rgx.match(stringToMatch)):
      # print("Match")
      return True
    else:
      # print("No match")
      return False
  else:
    print("Parameter [type:'{}'] [param:'{}']".format(type(stringToMatch), stringToMatch))
    return False