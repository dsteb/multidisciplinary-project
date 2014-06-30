#!/bin/bash
for i in `seq 2 10`; do
	scp azureuser@hadoop$i:~/mdp/mdp/stackoverflow/* ~/mdp/mdp/stackoverflow/ 
	scp azureuser@hadoop$i:~/mdp/mdp/github/* ~/mdp/mdp/github/ 
done

