"""
COURSE  :   EEE4121F    MOBILE AND WIRELESS NETWORKS 
AUTHOR  :   NATHANAEL THOMAS
STDNUM  :   THMNAT011
DATE    :   11 MAY 2022 
"""

import sys
import random
import time

#--------------------------------------------------------------------------------------------------------------------------------
#The following graph class was adapted from the code in
#https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
#The original author the code was adapted from was Alexey Klochay
class Graph(object):
    def __init__(self, switches, init_network):
        self.switches = switches
        self.graph = self.network_creation(switches, init_network)
    #function to create the network     
    def network_creation(self, switches, init_network):
        graph = {} #creating a dictionary for the network links 
        #creating the switches in the dictionary 
        for switch in switches:
            graph[switch] = {}
        graph.update(init_network)#updating the dictionary for the grap
        
        for switch, edges in graph.items():
            for adjacent_switch, value in edges.items():
                if graph[adjacent_switch].get(switch, False) == False:
                    graph[adjacent_switch][switch] = value         
        return graph
    #function to get the switches
    def get_switches(self):  
        return self.switches
    #getting the edges of the graph
    def get_outgoing_edges(self, switch):
        connections = []
        for out_switch in self.switches:
            if self.graph[switch].get(out_switch, False) != False:
                connections.append(out_switch)
        return connections
    #getting the values for the links 
    def value(self, switch1, switch2):
        "Returns the value of an edge between two switches."
        return self.graph[switch1][switch2]
    
    def dijkstra_algorithm(graph, start_switch):
        unvisited_switches = list(graph.get_switches())   
        shortest_path = {} #this dictionary will save the cost of visiting each switch the graph
        previous_switches = {} #this dictionary will save the shortest known path 
           
        max_value = sys.maxsize
        for switch in unvisited_switches:
            shortest_path[switch] = max_value
        # However, we initialize the starting switch's value with 0   
        shortest_path[start_switch] = 0
        
        # this will run until all the switches have been visited
        while unvisited_switches:
            # Find the link with the smallest cost 
            current_min_switch = None
            for switch in unvisited_switches: # go over the switches
                if current_min_switch == None:
                    current_min_switch = switch
                elif shortest_path[switch] < shortest_path[current_min_switch]:
                    current_min_switch = switch      
            # will update the current switch and the cost to the neighboring switch
            neighbors = graph.get_outgoing_edges(current_min_switch)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_switch] + graph.value(current_min_switch, neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # update to the lowest cost to the current switch
                    previous_switches[neighbor] = current_min_switch
            # Remove the switch that has been visited from the unvisted switch array
            unvisited_switches.remove(current_min_switch)
            print("Following switch connected to", current_min_switch);
        return previous_switches, shortest_path #will return an array of all the visited switches with the lowest cost and the shortest path
    #printing the results from the switch
    def print_result(previous_switches, shortest_path, start_switch, target_switch):
        path = []   #initialising an empty array
        switch = target_switch
        ttl = 0 #initialisng the time to live 
        while switch != start_switch:
            path.append(switch)
            switch = previous_switches[switch]
            ttl = ttl+1
        # Add the start switch manually
        path.append(start_switch)
        #Joining the shortest path and the cost of the sending the packet from source to destination
        value = format(shortest_path[target_switch])
        pathway = " -> ".join(reversed(path))
        hops = ttl
        return value, pathway, hops 
#------------------------------------------------------------------------------------------------------------------------------
#creating the links in the network
def create_links():
    print("The values for the links are")
    #switches in the network
    switches = ["s1", "s2", "s3", "s4", "s5"]
    init_network = {} #dictionary 
    for switch in switches:
        init_network[switch] = {}
    #initialising the links and randomly allocating weights to emulate how a real network will act 
    a = random.randint(1,10)
    print("the value between the s1 and s2 is: ", a)
    init_network["s1"]["s2"] = a 
    b = random.randint(1,10)
    print("the value between the s1 and s5 is: ", b)
    init_network["s1"]["s5"] = b
    c = random.randint(1,10)
    print("the value between the s2 and s5 is: ", c)
    init_network["s2"]["s5"] = c
    d = random.randint(1,10)
    print("the value between the s5 and s4 is: ", d)
    init_network["s5"]["s4"] = d
    e = random.randint(1,10)
    print("the value between the s1 and s3 is: ", e)
    init_network["s1"]["s3"] = e
    f = random.randint(1,10)
    print("the value between the s2 and s4 is: ", f)
    init_network["s2"]["s4"] = f
    g = random.randint(1,10)
    print("the value between the s3 and s4 is: ", g)
    init_network["s3"]["s4"] = g
    return switches, init_network
#function used to find which switch the hosts are connected to 
def find_switch(i):
    #intialising the hosts and switches linked 
    connections = ["h1","s1","h2","s1","h3","s2","h4","s2","h5","s3","h6","s3","h7","s4","h8","s5"]
    host = "h"+ str(i)
    x = connections.index(host)
    switch = connections[x+1]
    return switch
#function to return the ip address of a host
def get_ip(i):
    ip_add = "10.0.0.0." + str(i)
    return ip_add

#creating the graph
switches, init_network = create_links()
graph = Graph(switches, init_network)

#function to emulate the packet being sent to find the shortest path 
def packets(switch_src, switch_dst):
    begin = time.time() #start time 
    time.sleep(random.randint(1,3))
    #Getting the switches and shortest path, value, path taken and hops from the from the graph glass 
    previous_switches, shortest_path = Graph.dijkstra_algorithm(graph=graph, start_switch=switch_src)
    value, pathway, hops = Graph.print_result(previous_switches, shortest_path, start_switch=switch_src, target_switch=switch_dst)
    end = time.time() #endtime 
    duration = end-begin # finding the duration
    return value, pathway, hops, duration
#function to retrieve and print out the information from the packet 
def printPacket(s, s_ip,s_h, d, d_ip, d_h):
    value, pathway, hops, duration = packets(switch_src = s,switch_dst = d)
    print("-----------INFORMATION EXTRACTED FROM PACKET HEADER------------------------")
    print("---------------------------PACKET_HEADER-----------------------------------")
    print("---------------------------------------------------------------------------")
    print("SOURCE HOST INFORMATION")
    print("Source Host is : ",s_h)
    print("With IP Address of : ", s_ip)
    print("Connected to Switch : ",s)
    print("---------------------------------------------------------------------------")
    print("DESTINATION HOST INFORMATION")
    print("Destination Host is : ",d_h)
    print("With IP Address of : ", d_ip)
    print("Connected to Switch : ",d)
    print("----------------------------------------------------------------------------")
    print("The lowest cost to send packets from ",s_h, " to ",d_h," is ",value)
    print ("It to ", hops, "hops from source to destination")
    print("It took ",duration, " seconds to send the packet from source to destination")
    print("The shortest path the from source to destination is ", pathway)
    print("----------------END OF PACKET------------------------------------------------")

#main function to emulate sending packets from one host to another 
def main():
    print("WELCOME TO PACKET SENDING IMPROVED TRACEROUTE PROTOCOL")
    print("CREATING THE NETWORK")
   
    print("THE NETWORK HAS BEEN CREATED")

    src = input("Please chose a number between 1-8 for the sources host:\n")
    #to check for validiy of the input 
    if int(src) > 8:
        a = "h"+str(src)
        #Termination message
        print("No source host ",a, "available packet sending FAILED")
        print("Programmed closed")
    else:
        dst = input("Please chose a number between 1-8 for the destination host: \n")
        #to check for validiy of the input 
        if int(dst)>8:
            #termination message
            a = "h"+str(dst)
            print("No destination host ",a, "available packet sending FAILED")
            print("Programmed closed")
        else:
            #instatiating the source host
            src_host = "h"+str(src) 
            switch_src = find_switch(i=src) #finding the host switch
            switch_src_ip = get_ip(i=src) #finding the ip address of the sources 
            #instantiating the destination host
            dst_host = "h"+str(dst) 
            switch_dst = find_switch(i=dst) #finding the destination switch
            switch_dst_ip = get_ip(i=dst) #finding the ip address of the destination
            #info sent to host when sending the packet
            print("NOW SENDING DUMMY PACKET THROUGH THE NETWORK")
            print("Finding the shortest route")
            print("Shortest route found")
            print("PACKET INFORMATION EXTRACTED AND SHOWN BELOW")
            #printing the packet information to the host 
            printPacket(s=switch_src, s_ip=switch_src_ip,s_h=src_host, d=switch_dst, d_ip=switch_dst_ip, d_h=dst_host)
            print("PROGRAM DONE") 
            print("PACKETS RECIEVED BY HOST ", dst_host," FROM HOST",src_host)
            print("GOODBYE!!!!")
#running the main function
main()