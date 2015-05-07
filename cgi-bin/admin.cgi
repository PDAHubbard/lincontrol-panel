#!/bin/bash
#
#	Auto-redirect to this page for authentication and to log in
#


echo "content-type: html"
echo ""
if [ "$REMOTE_USER" != "admin" ]
then
	#echo "<html><head><body onload='window.location.href=/cgi-bin/bash.cgi'></body></head></html>"
	echo "<html><head><meta http-equiv=refresh content='0;URL=/cgi-bin/bash.cgi'></head></html>"
else

cat <<EOF
<html><head><title>Lincontrol admin panel</title></head></html><body>

                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
                <link href="/css/bootstrap.min.css" rel="stylesheet">
                <!--[if lt IE 9]>
                        <script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
                <![endif]-->
                <link href="/css/styles.css" rel="stylesheet">

<div id="top-nav" class="navbar navbar-inverse navbar-static-top">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">Administrator's Dashboard</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav navbar-right">
                <li class="dropdown">
                    <a class="dropdown-toggle" role="button" data-toggle="dropdown" href="#"><i class="glyphicon glyphicon-user"></i>$REMOTE_USER<span class="caret"></span></a>
                </li>
                <li><a href="/index.html#logout"><i class="glyphicon glyphicon-lock"></i> Logout</a></li>
            </ul>
        </div>
    </div>
    <!-- /container -->
</div>
EOF


USERNAME=`echo "$QUERY_STRING" | sed -n 's/^.*username=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
PASSWORD=`echo "$QUERY_STRING" | sed -n 's/^.*password=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
HTPASSFL=/var/www/lincontrol/.htpasswd

if [ -n "$USERNAME" ] && [ -n "$PASSWORD" ]
then
	# Check if the user is already in the file
	EXISTS=`grep $USERNAME $HTPASSFL`

	if [ -z "$EXISTS" ]
	then
		# run htpasswd
		htpasswd -b $HTPASSFL $USERNAME $PASSWORD 
		echo "<font color=red>New user $USERNAME added.</font><br>"
	else
		echo "User $USERNAME already exists.</br>"
	fi
fi

cat <<EOF
 <div class="panel panel-default">
         <div class="panel-heading">
               <h4>Add New User</h4></div>
                        <div class="panel-body">
			<form name=newuser method=get>
			Username <input type=text name=username id=username>
			Password <input type=password name=password id=password>
			<input type=submit>
			</form>
			</div>
	</div>
 </div>

 <div class="panel panel-default">
    <div class="panel-heading">
         <h4>Current users</h4>
               <div class="panel-body">
EOF

while read line
do
	THISUSER=`echo $line | awk -F":" '{print $1}'`
	echo "$THISUSER<br/>"
done < $HTPASSFL

cat <<EOF
	</div>
    </div>
 </div>
EOF


# create user

# delete user

# change password

echo "</body></html>"
fi

