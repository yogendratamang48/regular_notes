## Container Networking
## Building a Secure Swarm
### Big Picture:
- Two parts: Secured Cluster, Orchestrator
Secure Swarm Cluster
- MLS
- Native Swarm + Kubernetics
### Deep Dive
- SwarmKit
#### Old
- Single Engine Mode
- Swarm Mode
#### 
- Manager 
 - >`docker swarm join`
- One Manger Leader per swarm, Other Follower
- Raft Consensus Group
- Manager HA best practice: 3, 5 or 7
