from enum import *
import string

class JsonValue:
	class ValueType(Enum):
		ARRAY = 1
		FALSE = 2
		NULL = 3
		NUMBER = 4
		OBJECT = 5
		STRING = 6
		TRUE = 7
	def __init__(self, type):
		self.valueType = type
	def getValueType(self):
		return self.valueType
class JsonObject(JsonValue):
	def __init__(self):
		self.values = {}
		JsonValue.__init__(self, JsonValue.ValueType.OBJECT)
	def setValue(self, name, value):
		self.values[name] = value
	def getBoolean(self, name):
		return self.values[name]
	def getBoolean(self, name, defaultValue):
		if name in self.values:
			return self.values[name]
		else:
			return defaultValue
	def getInt(self, name):
		return self.values[name]
	def getInt(self, name, defaultValue):
		if name in self.values:
			return self.values[name]
		else:
			return defaultValue;
	def getJsonArray(self, name):
		return self.values[name]
	def getJsonNumber(self, name):
		return self.values[name]
	def getJsonObject(self, name):
		return self.values[name]
	def getJsonString(self, name):
		return self.values[name]
	def getString(self, name):
		return self.values[name]
	def getString(self, name, defaultValue):
		if name in self.values:
			return self.values[name]
		else:
			return defaultValue
	def isNull(self, name):
		return self.values[name].getValueType == ValueType.NULL
	def __str__(self):
		val = ""
		itr = False
		for attr in self.values:
			newline = ""
			if itr:
				newline = "\n"
			val = val + newline + attr + ": " + self.values[attr].__str__()
			itr = True
		return val
class JsonArray(JsonValue):
	def __init__(self):
		JsonValue.__init__(self, JsonValue.ValueType.ARRAY)
		self.values = []
	def setValue(self, index, value):
		self.values[index] = value
	def addValue(self, value):
		self.values.append(value)
	def getBoolean(self, index):
		val = self.values[index]
		if val.getValueType == JsonValue.ValueType.TRUE:
			return True
		else:
			return False
	def getBoolean(self, index, defaultValue):
		val = self.values[index]
		if val.getValueType == JsonValue.ValueType.TRUE:
			return True
		elif val.getValueType == JsonValue.ValueType.FALSE:
			return False
		else:
			return defaultValue
	def getInt(self, index):
		return getJsonNumber().intValue()
	def getInt(self, index, defaultValue):
		val = self.values[index]
		if val.getValueType == JsonValue.ValueType.NUMBER:
			return val.intValue
	def getJsonArray(self, index):
		return self.values[index]
	def getJsonNumber(self, index):
		return self.values[index]
	def getJsonString(self, index):
		return self.values[index]
	def getString(self, index):
		return getJsonString(index).getString
	def getString(self, index, defaultValue):
		val = self.values[index]
		if val.getValueType == JsonValue.ValueType.STRING:
			return val.getString
		return defaultValue
	def isNull(self, index):
		return self.values[index].getValueType == JsonValue.ValueType.NULL
	def __str__(self):
		val = ""
		itr = False
		for v in self.values:
			newline = ""
			if itr:
				newline = ", "
			val = val + newline + v.__str__()
			itr = True
		return val
class JsonString(JsonValue):
	def __init__(self, str):
		self.string = str
		JsonValue.__init__(self, JsonValue.ValueType.STRING)
	def getString(self):
		return self.string
	def __str__(self):
		return self.string
class JsonNumber(JsonValue):
	def __init__(self, num):
		self.number = num
		JsonValue.__init__(self, JsonValue.ValueType.NUMBER)
	def intValue(self):
		return self.number
	def __str__(self):
		return str(self.number)
class JsonBoolean(JsonValue):
	def __init__(self, bool):
		type = JsonValue.ValueType.FALSE
		if bool:
			type = JsonValue.ValueType.TRUE
		JsonValue.__init__(self, type)


class TokenType:
	LBRACE = 1
	RBRACE = 2
	LBRACKET = 3
	RBRACKET = 4
	STRING = 5
	NUMBER = 6
	BOOLEAN = 7
	COLON = 8
	COMMA = 9
class Token:
	def __init__(self, type, value):
		self.value = value
		self.type = type
	def getValue(self):
		return self.value
	def getType(self):
		return self.type
	def __str__(self):
		return "[" + str(self.type) + ", " + self.value + "]"

def readJSON(filename):
	validNumberChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', 'e', 'E']
	# Read and tokenize
	with open(filename, 'r') as file:
		jsonStr = file.read().replace('\n', '')
	tokens = []
	charCount = len(jsonStr)
	pointer = 0
	while pointer < charCount:
		c = jsonStr[pointer]
		if c == '{':
			tokens.append(Token(TokenType.LBRACE, '{'))
			pointer += 1
		elif c == '}':
			tokens.append(Token(TokenType.RBRACE, '}'))
			pointer += 1
		elif c == '[':
			tokens.append(Token(TokenType.LBRACKET, '['))
			pointer += 1
		elif c == ']':
			tokens.append(Token(TokenType.RBRACKET, ']'))
			pointer += 1
		elif c == ':':
			tokens.append(Token(TokenType.COLON, ':'))
			pointer += 1
		elif c == ',':
			tokens.append(Token(TokenType.COMMA, ','))
			pointer += 1
		elif c == '"':
			start = pointer
			end = jsonStr.find('"', pointer + 1)
			while jsonStr[end - 1] == '\\':
				end = jsonStr.find('"', end + 1)
			tokens.append(Token(TokenType.STRING, jsonStr[start + 1:end]))
			pointer = end + 1
		elif c == 't' and jsonStr[pointer + 1] == 'r' and jsonStr[pointer + 2] == 'u' and jsonStr[pointer + 3] == 'e':
			tokens.append(Token(TokenType.BOOLEAN, True))
			pointer += 4
		elif c == 'f' and jsonStr[pointer + 1] == 'a' and jsonStr[pointer + 2] == 'l' and jsonStr[pointer + 3] == 's' and json[pointer + 4] == 'e':
			tokens.append(Token(TokenType.BOOLEAN, False))
			pointer += 5
		elif c == ' ' or c == '\t' or c == '\n':
			pointer += 1
		else:
			start = pointer
			end = pointer
			while jsonStr[end] in validNumberChars:
				end += 1
			tokens.append(Token(TokenType.NUMBER, int(jsonStr[start:end-1])))
			pointer = end
	# Read tokens
	first = tokens.pop(0)
	print(first)
	if first.getType() == TokenType.LBRACE:
		return parse_Object(tokens)
	else:
		return None

def parse_Object(tokens):
	obj = JsonObject()
	while len(tokens) > 0:
		token = tokens.pop(0)
		if token.getType() == TokenType.RBRACE:
			break
		if token.getType() == TokenType.COMMA:
			token = tokens.pop(0)
		name = token.getValue()
		tokens.pop(0) # Pop the colon
		value = parse_Value(tokens)
		if value != None:
			obj.setValue(name, value)
	return obj
def parse_Value(tokens):
	if len(tokens) == 0:
		return None
	token = tokens.pop(0)
	if token.getType() == TokenType.BOOLEAN:
		return JsonBoolean(token.getValue())
	if token.getType() == TokenType.NUMBER:
		return JsonNumber(token.getValue())
	if token.getType() == TokenType.STRING:
		return JsonString(token.getValue())
	if token.getType() == TokenType.LBRACE:
		return parse_Object(tokens)
	if token.getType() == TokenType.LBRACKET:
		return parse_Array(tokens)
	return JsonValue(JsonValue.ValueType.NULL)
def parse_Array(tokens):
	arr = JsonArray()
	while len(tokens) > 0:
		token = tokens[0]
		if token.getType() == TokenType.RBRACKET:
			break
		if token.getType() == TokenType.COMMA:
			tokens.pop(0)
		val = parse_Value(tokens)
		if val != None:
			arr.addValue(val)
	return arr