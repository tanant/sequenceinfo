
digits_with_optional_dots = r'(?P<head>.*\.)(?P<digits>[0-9]+)(?P<tail>\..*)'
# standard type, separated file with dots

dcf_format_digital_stills = r'(?P<head>.*)(?P<digits>[0-9]{4})(?P<tail>\..*)'
# complex type, these follow a pattern where the file name is four alphanums
# with a trailing number. Notably, you can have: IMG_1239 OR you can have
# POO231234 in this format and both are valid
# DCF2.0 also allows a leading _ for alt colourspace files.

