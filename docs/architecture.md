# Architecture

## Connections

You can find these under `src/packages/eighballer/connections`

### `eightballer/ocean:0.1.0` Connection
This connection acts as a translation layer between the agent and the Ocean network. 
The main task of this connection is to act as a wrapper for the `ocean_lib` library, that is responsible for the actual communication with the ocean network.

### `eightballer/storj_file_transfer:0.1.0` Connection

This connection acts as a translation layer between the agent and the StorJ storage grid. 
The main task of this connection is to connect and mediate the file transfers to Storj.

## Skills

You can find these under `src/packages/eighballer/skills`

### `eightballer/ocean:0.1.0` Skill

The behaviours of this skill is what dictate the whole flow which the agent goes through.
There are 3 classes that define the behaviours of this skill `OceanC2DBehaviour`, `OceanDataAccessBehaviour` and `OceanDemoBehaviour`.
5 states are available for the agent to go through are already mentioned above. It's worth noting that the agent is can only be on one of those states at once.
The states are split into two classes `OceanC2DBehaviour` and `OceanDataAccessBehaviour`. 
`OceanC2DBehaviour` handles the first 4 states, whereas `OceanDataAccessBehaviour` handles the last one.
`OceanDemoBehaviour` is responsible for handling the switch between the two above-mentioned classes.

### `eightballer/storj_file_uploader:0.1.0` Skill

Very simple behaviour where the agent reads and searializes the file that needs to be uploaded into an Envelope with bytes content.

## Protocols

You can find these under `src/packages/eighballer/protocols`

### `eightballer/ocean:0.1.0` Protocol
This protocol is in place to allow for communication between the different components of the agent, in this case between the above mentioned connection and skill.

### `eightballer/file_storage:0.1.0` Protocol

This protocol is in place to allow for communication between the different components of the agent, in this case between the above mentioned connection and skill.