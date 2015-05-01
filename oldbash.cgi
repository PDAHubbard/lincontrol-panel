#!/bin/sh
    echo "Content-type: text/html\n"
     
    # read in our parameters
    CMD=`echo "$QUERY_STRING" | sed -n 's/^.*cmd=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
    FOLDER=`echo "$QUERY_STRING" | sed -n 's/^.*folder=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
     FOLDER1=`echo "$QUERY_STRING" | sed -n 's/^.*folder1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
FOLDER2=`echo "$QUERY_STRING" | sed -n 's/^.*folder2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`

    # our html header
    echo "<html>"
    echo "<head><title>Bash CGI</title></head>"
    echo "<body>"
     
    # test if any parameters were passed
    if [ $CMD ]
    then
      case "$CMD" in
        ifconfig)
          echo "Output of ifconfig :<pre>"
          /sbin/ifconfig
          echo "</pre>"
          ;;
     
            lsal)
              echo "Output of ls $FOLDER1 :<pre>"
              /bin/ls -al "$FOLDER1"
              echo "</pre>"
              ;;

         *)
          echo "Unknown command $CMD<br>"
          ;;
      esac
    fi
     
    # print out the form
     
    # page header
    echo "<p>"
    echo "<center>"
    echo "<h2>Bash commands</h2>"
    echo "</center>"
    echo "<p>"
    echo "<p>"
     
    echo "Choose which command you want to run"
    echo "<form method=get>"
    echo "<input type=radio name=cmd value=ifconfig checked> ifconfig (Network configuration) <br>"
    echo "<input type=radio name=cmd value=lsal> ls -al -- folder <input type=text name=folder1 value=/mnt/flash><br>"
echo "<input type=radio name=cmd value=wol> wakeonlan (enter mac address) <input type=text name=folder2 value=00:00:00:00:00:00><br>"
    echo "<input type=submit>"
    echo "</form>"
    echo "</body>"
    echo "</html>"
