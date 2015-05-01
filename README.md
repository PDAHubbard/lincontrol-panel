# lincontrol-panel

## INSTALL

Copy both .cgi files to the /cgi-bin/ folder of your website
Ensure both files are executable
Ensure CGI module is enabled in the Apache configs
Browse to http://site.name/cgi-bin/bash.cgi

## CONFIGURATION
Configure the Service name, Config file in 'bash.cgi':
    CONFIG_FILE=<full path to config file>
    SERVICE_NAME=<name of the service>

Add commands to start, stop and restart the service at lines 163-175

Configure the log file to be viewed in 'logviewer.cgi':
    LOG_FILE=<full path to log file>

Refresh interval of the log viewer can be changed at
    <meta http-equiv="refresh" content="30">
The "content" value is the refresh interval in seconds.

## REQUIREMENTS
1. CONFIG_FILE must be writable by the webserver user (ie. www-data)
2. Commands for start/stopping the process must be runnable by the webserver user.

## TODO
1. Add information for htaccess security
2. Add functionality to prevent inadvertant alteration
3. Allow user to reset the textarea box
4. Add styling to make better use of space.
5. Workaround setuid limitation with C program to call service script.


## Example Apache VirtualHost config
...
        ErrorLog ${APACHE_LOG_DIR}/lincontrol_error.log
        CustomLog ${APACHE_LOG_DIR}/lincontrol_access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

        ScriptAlias /cgi-bin/ /var/www/lincontrol/cgi-bin/
        AddHandler cgi-script .cgi .pl

        <Directory /var/www/lincontrol/>
                AuthType Basic
                AuthName "Private"
                AuthUserFile "/usr/local/apache/passwd/lincontrol_passwords"
                Require user user2
        </Directory>

