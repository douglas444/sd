from enum import Enum;
import time;
import pickle;

MINUTES_BETWEEN_SNAPSHOTS = 1;

class SnapshoterState(Enum):
    BLOCKED = 1;
    SAVING_SNAPSHOT = 2;
    DELETING_LOG = 3;

class Snapshoter(object):
    def __init__(self, dataBase):
        self.dataBase = dataBase;
        try:
            State_file = open('snapshoter_state','r');
        except FileNotFoundError:
            self.SnapshoterState = SnapshoterState.BLOCKED;
        else:
            self.SnapshoterState = SnapshoterState[State_file.read()];
            State_file.close();


    def startSnapshoter(self):
        if(self.SnapshoterState == SnapshoterState.BLOCKED):
            self.block();
        elif(self.SnapshoterState == SnapshoterState.SAVING_SNAPSHOT):
            self.saveSnapshot();
        elif(self.SnapshoterState == SnapshoterState.DELETING_LOG):
            self.deleteLog();
            
        while (True):
            self.block();


    def changeSnapshoterState(self,SnapshoterState):
        self.SnapshoterState = SnapshoterState;
        with open('snapshoter_state','w') as SnapshoterState_file:
            SnapshoterState_file.write(self.SnapshoterState.name);

    def block(self):
        time.sleep(60 * MINUTES_BETWEEN_SNAPSHOTS);
        self.changeSnapshoterState(SnapshoterState.SAVING_SNAPSHOT);
        self.saveSnapshot();

    def saveSnapshot(self):
        with open('snapshot','wb') as snap_file:
            pickle.dump(self.dataBase.getHash(), snap_file, pickle.HIGHEST_PROTOCOL);
        self.changeSnapshoterState(SnapshoterState.DELETING_LOG);
        print("snapshot saved");
        self.deleteLog();

    def deleteLog(self):
        with open('log','w'):
            pass;
        self.changeSnapshoterState(SnapshoterState.BLOCKED);


    def loadSnapshot(self):
        try:
            with open('snapshot','rb') as snap_file:
                self.dataBase.putHash(pickle.load(snap_file));
        except FileNotFoundError:
            pass;

    def getState(self):
        return self.SnapshoterState;
