# Swiss Tournament Round 1-2

This program will simulate the first two rounds of a Swiss Tournament. In the first round
each player will be randomly assigned to another and a win or loss will be recorded. In the second
round, those players who have one win will play one another and those with one loss will play one another. 

<h3>Install Virtualbox</h3>
https://www.virtualbox.org/wiki/Downloads<br>
</p>

<h3>Install Vagrant</h3>
https://www.vagrantup.com/downloads<br>
</p>

<p>
Verify that Vagrant is installed and working by typing in the terminal: <br>
$ vagrant -v<br>
# will print out the Vagrant version number<br>
</p>

<h3>Clone the Repository</h3>
Once you are sure that VirtualBox and Vagrant are installed correctly execute the following:

$ git clone https://github.com/p00gz/udacity-swiss-tournament.git<br>
$ cd udacity-swiss-tournament<br>
$ cd vagrant

<h3>Verify that these files exist in the root of the newly cloned repository:</h3><br>
<pre>
--tournament             #folder containing tournament files
----tournament.py        #file that contains the python functions which unit tests will run on
----tournament_test.py   #unit tests for tournament.py
----tournament.sql       #postgresql database
--Vagrantfile            #template that launches the Vagrant environment
--pg_config.sh           #shell script provisioner called by Vagrantfile that performs
                          some configurations 
</pre

<h3>Launch the Vagrant Box</h3>
<pre>
$ vagrant up #to launch and provision the vagrant environment
$ vagrant ssh #to login to your vagrant environment
</pre>

<h3>Run the tests on the Swiss Tournament</h3>
<pre>
$ cd tournament
$ python tournament_test.py
</pre>

you should see these results:
<pre>
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!
</pre>
