# Badnick Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.8'


import b3, time, threading, thread
import b3.events
import b3.plugin

class BadnickPlugin(b3.plugin.Plugin):

    _adminPlugin = None

    def onLoadConfig(self):
    
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self._minlevel = self.config.getint('settings', 'minlevel')
        self._badnickminlevel = self.config.getint('settings', 'badnickminlevel')
        self._protectlevel = self.config.getint('settings', 'protectlevel')
        
        self._adminPlugin.registerCommand(self, 'badnick',self._minlevel, self.cmd_badnick)
        self._adminPlugin.registerCommand(self, 'addbadnick',self._badnickminlevel, self.cmd_addbadnick, 'addbn')
        self._adminPlugin.registerCommand(self, 'addverybadnick',self._badnickminlevel, self.cmd_addverybadnick, 'addvbn')
        
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.registerEvent(b3.events.EVT_CLIENT_NAME_CHANGE)
    
    def onEvent(self, event):
        
        if (event.type == b3.events.EVT_CLIENT_AUTH) or (event.type == b3.events.EVT_CLIENT_NAME_CHANGE):
            
            sclient = event.client
            data = 'none'
            cnamemin = sclient.name.lower()
           
            if (sclient.name.isdigit()) or (len(sclient.name) < 2) or ('//' in cnamemin):
                
                ban='no'
                name = sclient.name        
                thread.start_new_thread(self.cmdbadnick, (data, sclient, name, ban))

            cursor = self.console.storage.query("""
            SELECT *
            FROM badnick
            """)
        
            c = 1
        
            if cursor.EOF:
          
                cursor.close()            
            
                return False
        
            while not cursor.EOF:
            
                sr = cursor.getRow()
                nick = sr['nick']
                ban = sr['ban']
            
                if cnamemin == nick:
                
                    name = sclient.name        
                    thread.start_new_thread(self.cmdbadnick, (data, sclient, name, ban))
               
                cursor.moveNext()
            
            c += 1
            
        cursor.close()
    
    def cmd_badnick(self, data, client, cmd=None):
        
        """\
        <name> - Player name with Bad Nickname
        """
        
        ban = 'no'
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!badnick <player name>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if not sclient:
            
            return False
      
        if sclient.maxLevel >= self._protectlevel:
            
            client.message('^3Invalid Command on %s!' %(sclient.exactName))
            return False

        if sclient:        
            
            name = sclient.name        
            thread.start_new_thread(self.cmdbadnick, (data, sclient, name, ban))
            
        else:
            return False
    
    def cmdbadnick(self, data, sclient, name, ban):

        if data == 'none':

            time.sleep(10)

        if ban == 'no':
        
            reps = 3
            
            self.console.say('%s^1 Bad Nickmane !'%(sclient.exactName))
            
            while reps > 0:
                
                for cid,x in self.console.clients.items():

                    if x == sclient:
                        
                        if name == sclient.name :
                                    
                            self.console.write('forceteam %s %s' %(sclient.cid, 's'))
                            self._adminPlugin.warnClient(sclient, '^3Bad NickName', None, False, '', 60)
                            sclient.message('^3Change your NickName !')       
                        else:
                            return False
            
                time.sleep(20)
                reps-=1
        
        if ban == 'yes' :
    
            sclient.message('%s^1 as nickname is not authorized'%(sclient.exactName))
            sclient.message('^1You will be banned ! ^3Kenavo !')
            time.sleep(5)
            sclient.ban("Very Bad Nickname !", None)    
    
    def cmd_addbadnick(self, data, client, cmd=None):
    
        """\
        Add bad nickname <nick mane>
        """

        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!addbadnick <nick name>')
            
            return
        
        cdata=input[0]
  
        if cdata:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM badnick n 
            WHERE n.nick = '%s'
            """ % (cdata))

            if cursor.rowcount > 0:
                
                client.message('This Bad Nickname is already registered')
                cursor.close()
                
                return False
            
            cursor.close()
        
            cursor = self.console.storage.query("""
            INSERT INTO badnick
            VALUES ('%s', 'no')
            """ % (cdata))
            
            cursor.close()
            client.message('Bad Nickname is now registered')
       
        else:
            return False

    def cmd_addverybadnick(self, data, client, cmd=None):
    
        """\
        Add very bad nickname <nick mane>
        """

        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!addverybadnick <nick name>')
            
            return
        
        cdata=input[0]
  
        if cdata:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM badnick n 
            WHERE n.nick = '%s'
            """ % (cdata))

            if cursor.rowcount > 0:
                
                client.message('This Very Bad Nickname is already registered')
                cursor.close()
                
                return False
            
            cursor.close()
        
            cursor = self.console.storage.query("""
            INSERT INTO badnick
            VALUES ('%s', 'yes')
            """ % (cdata))
            
            cursor.close()
            client.message('Very Bad Nickname is now registered')
       
        else:
            return False
