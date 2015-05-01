#!/bin/bash

LOG_FILE=/var/log/messages



GREP_STRING=`echo "$QUERY_STRING" | sed -n 's/^.*grep=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
NUMLINES=`echo "$QUERY_STRING" | sed -n 's/^.*numlines=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

echo "Content-type: text/html"
echo ""

cat <<EOF
<html>
<head>
<meta http-equiv="refresh" content="30">
</head>
<body>

<form method=get>
<label for=grep>Search string</label>
<input name=grep>
<select name=numlines>
	<option value="">Lines</option>
	<option value="25">25</option>
	<option value="50">50</option>
	<option value="100">100</option>
	<option value="200">200</option>
	<option value="500">500</option>
	<option value="1000">1000</option>
</select>

<input type=submit>
</form>

<pre>
EOF

if [[ ! $NUMLINES ]]
then
	NUMLINES=25
fi


if [[ $GREP_STRING ]]
then
	tail -n $NUMLINES $LOG_FILE | grep "$GREP_STRING"
else
	tail -n $NUMLINES $LOG_FILE 
fi
cat <<EOF
</pre>
</body>
</html>
EOF

