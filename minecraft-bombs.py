#www.stuffaboutcode.com and @williamsthing
#Raspberry Pi, Minecraft Bombs - Turn any block into a bomb instantly!

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import threading, so threads can be used
import threading

class ExplodingBlock(threading.Thread):

    def __init__(self, pos, fuseInSecs, blastRadius):
        #Setup object
        threading.Thread.__init__(self)
        self.pos = pos
        self.fuseInSecs = fuseInSecs
        self.blastRadius = blastRadius

    def run(self):
        #Open connect to minecraft
        mc = minecraft.Minecraft.create()

        #Get values
        pos = self.pos
        blastRadius = self.blastRadius

        #Explode the block!
        # get block type
        blockType = mc.getBlock(pos.x, pos.y, pos.z)
        # create sphere of air
        for x in range(blastRadius*-1,blastRadius):
            for y in range(blastRadius*-1, blastRadius):
                for z in range(blastRadius*-1,blastRadius):
                    if x**2 + y**2 + z**2 < blastRadius**2:
                        mc.setBlock(pos.x + x, pos.y + y, pos.z + z, block.AIR)

if __name__ == "__main__":

    time.sleep(5)
    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    #Post a message to the minecraft chat window 
    mc.postToChat("Minecraft Bombs, Hit (Right Click) a Block Instantly! Made by www.stuffaboutcode.com and modded by @williamsthing")

    #loop until Ctrl C
    try:
        while True:
            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # if a block has been hit
            if blockHits:
                # for each block that has been hit
                for blockHit in blockHits:
                    #Create and run the exploding block class in its own thread
                    # pass the position of the block, fuse time in seconds and blast radius
                    # threads are used so multiple exploding blocks can be created
                    explodingBlock = ExplodingBlock(blockHit.pos, 3, 3)
                    explodingBlock.daemon
                    explodingBlock.start()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("stopped")
