#!/usr/bin/env python
# coding=utf-8
'''
Author        : zhenghaoming
Date          : 2022-02-27 18:07:56
FilePath      : \BooBoo\exp_app.py
version       : 
LastEditors   : zhenghaoming
LastEditTime  : 2022-02-28 09:10:00
'''
#!/usr/bin/env python
# coding=utf-8
import os,shutil
import logging
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
logging.basicConfig(filename = os.path.expanduser('~/btach_run.log'),
                    filemode = 'w',
                    level = logging.INFO,
                    format = '%(asctime)s [%(levelname)s] %(message)s',
                    datefmt = '%Y/%m/%d %H:%M:%S')

logger = logging.getLogger()

def main(self,file_list,savefilepath,scriptfile):
    '''
    '''
    os.environ['MAYA_SKIP_USERSETUP_PY'] = str()

    step = 0
    step_val = 100 /(len(file_list))

    try:
        import maya.standalone
        maya.standalone.initialize(name='python')
    except:
        return


    import core_script
    for filePath in file_list:
        print ("The file name: %s\n" % filePath[0])
        print ("The full file name: %s\n" % filePath[1])
        print ("The savue path : %s\n" % savefilepath)
        print ("The script path : %s\n" % scriptfile)
        if self.render_chbox.isChecked():
            ren_check = 1
            if self.sequence_radioBtn.isChecked():
                ren_mod = 1
            else:
                ren_mod = 2
        else :
            ren_check = 0
        core_script.main(ren_check,ren_mod,filePath[0],filePath[1],savefilepath)

        step += step_val
        self.progressBar.setValue(step)

    maya.standalone.uninitialize()
    if os.path.isfile(("%s/Ren/temp/render_temp.bat" % (savefilepath))):
        os.system(("%s/Ren/temp/render_temp.bat" % (savefilepath)))
        mydir= ("%s/Ren/temp/render_temp.bat" % (savefilepath))
        try:
            shutil.rmtree(mydir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


# if __name__ == '__main__':
#     main(['D:/work/asset_exporter/example/test_scene.ma'])
