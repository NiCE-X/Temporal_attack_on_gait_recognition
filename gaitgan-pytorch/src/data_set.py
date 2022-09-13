import torch as th
import cv2
import numpy as np
import os


def loadImage(path):
    #print(path)
    inImage = cv2.imread(path, 0)
    info = np.iinfo(inImage.dtype)
    inImage = inImage.astype(np.float) / info.max

    iw = inImage.shape[1]
    ih = inImage.shape[0]
    if iw < ih:
        inImage = cv2.resize(inImage, (64, int(64 * ih/iw)))
    else:
        inImage = cv2.resize(inImage, (int(64 * iw / ih), 64))
    inImage = inImage[0:64, 0:64]
    return th.from_numpy(2 * inImage - 1).unsqueeze(0)


class CASIABDataset():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.ids = np.arange(1, 75)
        self.cond = ['bg-01', 'bg-02', 'cl-01', 'cl-02',
                     'nm-01', 'nm-02', 'nm-03', 'nm-04',
                     'nm-05', 'nm-06']
        self.angles = ['000', '018', '036', '054', '072',
                       '108', '126', '144', '162', '180']
        self.n_id = 74
        self.n_cond = len(self.cond)
        self.n_ang = len(self.angles)

    def getbatch(self, batchsize):
        batch1 = []
        batch2 = []
        batch3 = []
        for i in range(batchsize):
            seed = th.randint(1, 100000, (1,)).item()
            th.manual_seed((i+1)*seed)
            # r1 is GT target
            # r2 is irrelevant GT target
            # r3 is source image
            id1 = th.randint(0, self. n_id, (1,)).item() + 1
            id1 = '%03d' % id1
            # cond1 = th.randint(4, self.n_cond, (1,)).item()
            # cond1 = int(cond1)
            # cond1 = self.cond[cond1]
            cond1 = 'nm-01'
            r1 = id1 + '/' + cond1 + '/' + id1 + '-' + \
                cond1 + '-' + '090.png'
            #print(r1)

            id2 = id1
            while (id2 == id1):
                id2 = th.randint(0, self. n_id, (1,)).item() + 1
                id2 = '%03d' % id2
                # cond2 = th.randint(4, self.n_cond, (1,)).item()
                # cond2 = int(cond2)
                # cond2 = self.cond[cond2]
                cond2 = 'nm-01'
                r2 = id2 + '/' + cond2 + '/' + id2 + '-' + \
                    cond2 + '-' + '090.png'
                #print(r2)
            while True:
                angle = th.randint(0, self.n_ang, (1,)).item()
                angle = int(angle)
                angle = self.angles[angle]
                cond3 = th.randint(0, self.n_cond, (1,)).item()
                cond3 = int(cond3)
                cond3 = self.cond[cond3]

                r3 = id1 + '/' + cond3 + '/' + id1 + '-' + \
                    cond3 + '-' + angle + '.png'
                #print(r3)
                if os.path.exists(self.data_dir + r3):
                    break
                #else:
                    #print(self.data_dir + r3)

            img1 = loadImage(self.data_dir + r1)
            img2 = loadImage(self.data_dir + r2)
            img3 = loadImage(self.data_dir + r3)
            batch1.append(img1)
            batch2.append(img2)
            batch3.append(img3)
        return th.stack(batch1), th.stack(batch2), th.stack(batch3)


class CASIABDatasetForTest():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.ids = np.arange(75, 125)
        self.cond = ['bg-01', 'bg-02', 'cl-01', 'cl-02',
                     'nm-01', 'nm-02', 'nm-03', 'nm-04',
                     'nm-05', 'nm-06']
        self.angles = ['000', '018', '036', '054', '072',
                       '108', '126', '144', '162', '180']
        self.n_id = 62
        self.n_cond = len(self.cond)
        self.n_ang = len(self.angles)

    def getbatch(self, batchsize):
        batch1 = []
        batch2 = []
        batch3 = []
        for i in range(batchsize):
            seed = th.randint(1, 100000, (1,)).item()
            th.manual_seed((i+1)*seed)
            # r1 is GT target
            # r2 is irrelevant GT target
            # r3 is source image
            id1 = th.randint(0, self. n_id, (1,)).item() + 1
            id1 = '%03d' % id1
            # cond1 = th.randint(4, self.n_cond, (1,)).item()
            # cond1 = int(cond1)
            # cond1 = self.cond[cond1]
            cond1 = 'nm-01'
            r1 = id1 + '/' + cond1 + '/' + id1 + '-' + \
                cond1 + '-' + '090.png'

            id2 = id1
            while (id2 == id1):
                id2 = th.randint(0, self. n_id, (1,)).item() + 1
                id2 = '%03d' % id2
                # cond2 = th.randint(4, self.n_cond, (1,)).item()
                # cond2 = int(cond2)
                # cond2 = self.cond[cond2]
                cond2 = 'nm-01'
                r2 = id2 + '/' + cond2 + '/' + id2 + '-' + \
                    cond2 + '-' + '090.png'
            while True:
                angle = th.randint(0, self.n_ang, (1,)).item()
                angle = int(angle)
                angle = self.angles[angle]
                cond3 = th.randint(0, self.n_cond, (1,)).item()
                cond3 = int(cond3)
                cond3 = self.cond[cond3]

                r3 = id1 + '/' + cond3 + '/' + id1 + '-' + \
                    cond3 + '-' + angle + '.png'
                if os.path.exists(self.data_dir + r3):
                    break

            img1 = loadImage(self.data_dir + r1)
            img2 = loadImage(self.data_dir + r2)
            img3 = loadImage(self.data_dir + r3)
            batch1.append(img1)
            batch2.append(img2)
            batch3.append(img3)
        return th.stack(batch1), th.stack(batch2), th.stack(batch3)


class CASIABDatasetGenerate():
    def __init__(self, data_dir, cond):
        self.data_dir = data_dir
        self.ids = np.arange(75, 125)
        self.angles = ['000', '018', '036', '054', '072',
                       '108', '126', '144', '162', '180']
        self.n_ang = len(self.angles)
        self.cond = cond

    def getbatch(self, idx, batchsize):
        batch1 = []
        batch3 = []
        id1 = idx
        id1 = '%03d' % id1
        cond1 = self.cond
        r1 = id1 + '/' + cond1 + '/' + id1 + '-' + \
            cond1 + '-' + '090.png'
        img1 = loadImage(self.data_dir + r1)
        for angle in self.angles:
            # r1 is GT target
            # r2 is source image
            r3 = id1 + '/' + cond1 + '/' + id1 + '-' + \
                cond1 + '-' + angle + '.png'
            if not os.path.exists(self.data_dir + r3):
                img3 = th.from_numpy(np.zeros((64, 64))).unsqueeze(0)
            else:
                img3 = loadImage(self.data_dir + r3)
            
           
            batch1.append(img1)
            batch3.append(img3)
        return  th.stack(batch1), th.stack(batch3)
