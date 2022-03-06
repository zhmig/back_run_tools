#!/usr/bin/env python
# coding=utf-8

import re,os,logging,json
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup

logger = logging.getLogger()

# 加载arnold插件
def load_plugin(plugin_name):
    '''
    '''
    if not cmds.pluginInfo(plugin_name, q=True, l=True):
        try:
            cmds.loadPlugin(plugin_name)
        except:
            pass

# 导入json文件
'''
导出
def exportFile(filename):
    with open(filename, "w+") as file:
        json.dump(renderSetup.instance().encode(None), fp=file, indent=2, sort_keys=True)
'''
# Cannot name function "import", as this is a reserved Python keyword.
def importFile(rs,json_file):
    with open(json_file, "r") as file:
        rs.decode(json.load(file), renderSetup.DECODE_AND_OVERWRITE, None)

# 设置帧数时长范围
def time_range():
    start_frame = int(cmds.playbackOptions(q=True, min=True))
    end_frame = int(cmds.playbackOptions(q=True, max=True))

    return start_frame,end_frame

# 设置渲染设置，命名方式，帧数，尺寸，相机
def set_render_setting(start_frame,end_frame):
    # 设置渲染相机
    # 设置全部不可见
    # 获取相机并且剔除maya默认相机
    defaultCams = ["front" , "persp" , "side" , "top"]
    camera = list(set(defaultCams) ^ set(cmds.listCameras()))# 可以把两个列表做个差集保留不相同的部分
    #关闭所有相机的可见性
    [ cmds.setAttr("%s.renderable" % i,0) for i in defaultCams ]
    #打开需要渲染的相机可见性
    if len(camera) > 0:
        cmds.setAttr(("%s.renderable" % camera[0]),1)

    #渲染设置参数
    if cmds.objExists('defaultRenderGlobals'):
        default_render = pm.PyNode('defaultRenderGlobals')
        pm.listAttr(default_render)
    if cmds.objExists('defaultResolution'):
        resNode = pm.PyNode("defaultResolution")
        pm.listAttr(resNode)
    if not pm.objExists( "defaultArnoldDriver" ):
        createOptions()
    arDirver = pm.PyNode('defaultArnoldDriver')
    try:
        default_render.outFormatControl.set(0)
        default_render.animation.set(1)
        default_render.putFrameBeforeExt.set(1)
        default_render.extensionPadding.set(4)
        default_render.periodInExt.set(1)
        default_render.imageFilePrefix.set("<Scene>/<RenderLayer>/<RenderLayer>")
        default_render.startFrame.set(start_frame)
        default_render.endFrame.set(end_frame)

        cmds.setAttr('defaultResolution.width', 1920)
        cmds.setAttr('defaultResolution.height', 1080)

        cmds.setAttr('defaultRenderGlobals.ren', 'arnold', type='string')
        arDirver.ai_translator.set('exr')
        arDirver.halfPrecision.set(1)
        arDirver.exrTiled.set(0)
        arDirver.mergeAOVs.set(1)

    except:
        return

    # 设置主层不被渲染
    lay = cmds.editRenderLayerGlobals( q=True, crl=True )
    if 'defaultRenderLayer' in lay:
        cmds.setAttr( 'defaultRenderLayer.renderable', 0 )

# BG层
def bg_setting():
    displays = pm.ls("*::smooth",typ='displayLayer')
    if not displays:
        return

    for lay in displays:
        objs = pm.editDisplayLayerMembers(lay,q=True)
        if objs:
            for obj in objs:
                cmds.displaySmoothness(obj,du=3,dv=3,pw=16,ps=4,po=3)

# CH层
def ch_setting(rs):
    try: ch_rl = rs.getRenderLayer("color")
    except: ch_rl = rs.createRenderLayer("color")
    try: ch_c1 = ch_rl.getCollectionByName("ch")
    except:  ch_c1 = ch_rl.createCollection("ch")
    try: ch_mask_l = rs.getRenderLayer("mask")
    except: ch_mask_l = rs.createRenderLayer("mask")
    try: ch_mask_c1 = ch_mask_l.getCollectionByName("red")
    except:  ch_mask_c1 = ch_mask_l.createCollection("red")

    all_top_group = pm.ls(pm.ls(assemblies = True),typ = "transform",l=True)
    ch_group = []
    for grp in all_top_group:
        match  = re.match(r'ch',str(grp))
        if match is not None:
            ch_group.append("|%s" % grp)
            pm.displaySmoothness(grp,du=3,dv=3,pw=16,ps=4,po=3)

    ch_pattern = ','.join(map(str,ch_group))
    ch_staticSelection = ' '.join(map(str,ch_group))

    simple_select = cmds.listConnections("ch",type="simpleSelector")
    if simple_select:
        pattern = cmds.getAttr("%s.pattern" % simple_select[0])
        ch_col_pattern = ("%s,%s" % (ch_pattern,pattern))
        staticSelection = cmds.getAttr("%s.staticSelection" % simple_select[0])
        ch_col_staticSelection = ("%s %s" % (ch_staticSelection,staticSelection))
        ch_c1.getSelector().setPattern(ch_col_pattern)
        ch_c1.getSelector().setStaticSelection(ch_col_staticSelection)
    simple_select = cmds.listConnections("red",type="simpleSelector")
    if simple_select:
        pattern = cmds.getAttr("%s.staticSelection" % simple_select[0])
        ch_msk_pattern = ("%s,%s" % (ch_pattern,pattern))
        staticSelection = cmds.getAttr("%s.pattern" % simple_select[0])
        ch_msk_staticSelection = ("%s %s" % (ch_staticSelection,staticSelection))
        ch_mask_c1.getSelector().setPattern(ch_msk_pattern)
        ch_mask_c1.getSelector().setStaticSelection(ch_msk_staticSelection)

# PR层
def pr_setting(rs):
    try: pr_rl = rs.getRenderLayer("color")
    except: pr_rl = rs.createRenderLayer("color")
    try: pr_c1 = pr_rl.getCollectionByName("ch")
    except:  pr_c1 = pr_rl.createCollection("ch")
    try: pr_mask_l = rs.getRenderLayer("mask")
    except: pr_mask_l = rs.createRenderLayer("mask")
    try: pr_mask_c1 = pr_mask_l.getCollectionByName("green")
    except:  pr_mask_c1 = pr_mask_l.createCollection("green")
    all_top_group = pm.ls(pm.ls(assemblies = True),typ = "transform",l=True)
    pr_group = []
    for grp in all_top_group:
        match  = re.match(r'pr',str(grp))
        if match is not None:
            pr_group.append("|%s" % grp)
            pm.displaySmoothness(grp,du=3,dv=3,pw=16,ps=4,po=3)
    pr_pattern = ','.join(map(str,pr_group))
    pr_staticSelection = ' '.join(map(str,pr_group))

    simple_select = cmds.listConnections("ch",type="simpleSelector")
    if simple_select:
        pattern = cmds.getAttr("%s.pattern" % simple_select[0])
        pr_col_pattern = ("%s,%s" % (pr_pattern,pattern))
        staticSelection = cmds.getAttr("%s.staticSelection" % simple_select[0])
        pr_col_staticSelection = ("%s %s" % (pr_staticSelection,staticSelection))
        pr_c1.getSelector().setPattern(pr_col_pattern)
        pr_c1.getSelector().setStaticSelection(pr_col_staticSelection)
    simple_select = cmds.listConnections("green",type="simpleSelector")
    if simple_select:
        pattern = cmds.getAttr("%s.staticSelection" % simple_select[0])
        pr_msk_pattern = ("%s,%s" % (pr_pattern,pattern))
        staticSelection = cmds.getAttr("%s.pattern" % simple_select[0])
        pr_msk_staticSelection = ("%s %s" % (pr_staticSelection,staticSelection))       
        pr_mask_c1.getSelector().setPattern(pr_msk_pattern)
        pr_mask_c1.getSelector().setStaticSelection(pr_msk_staticSelection)

def _render(rencheck,mod,filename,savefilepath):
    start_frame,end_frame = time_range()
    minkey = (end_frame + start_frame)/2
    renderfile = ("C:/Program Files/Autodesk/Maya2019/bin/render.exe").replace("\\", "/")
    saveimage = ("%s/Ren/images/%s" % (savefilepath,filename[:-3]))
    if not os.path.isdir(saveimage):
        os.makedirs(saveimage)
    saveFile = ("%s/Ren/%srd.mb" % (savefilepath,filename[:-2]))
    bat_file = ("%s/Ren/temp/render_temp.bat" % savefilepath)

    if not os.path.isdir(os.path.split(bat_file)[0]):
        os.makedirs(os.path.split(bat_file)[0])

    command = ''
    if os.path.isfile(saveFile):
        if rencheck == 1:
            if mod == 1:
                command = ('"%s" -s %s -e %s -rd "%s" "%s"' % (renderfile,minkey,minkey, saveimage, saveFile))
            if mod == 2:
                command = ('"%s" -s %s -e %s -rd "%s" "%s"' % (renderfile,start_frame,end_frame, saveimage, saveFile))
            with open(bat_file,'a') as f:
                f.write(command + "\"\r\n")
            f.close()
        else:
            return

def main(rencheck,mod,filename,filePath,savefilepath):
    '''
    '''
    load_plugin('mtoa.mll')

    if not os.path.isfile(filePath):
        return

    logger.info(filePath)
    try:
        cmds.file(filePath, o=True, f=True)
    except RuntimeError as e:
        logger.info('Exception occurred', exc_info=True)

    from mtoa.core import * 

    mel.eval('setCurrentRenderer "arnold"')   

    rs = renderSetup.instance()  

    for f in cmds.file(q=True,r=True):
        if re.search(r'scenes',f):
            bg_file = f

    json_file = ("%s.json" % os.path.splitext(bg_file)[0])

    if os.path.isfile(json_file):
        importFile(rs,json_file) 
        ch_setting(rs)
        pr_setting(rs)
    else:
        logger.info('No Query Json File', exc_info=True)
        return

    start_frame,end_frame = time_range()
    set_render_setting(start_frame,end_frame)
    
    out_dir = ("%s/Ren" % (savefilepath))
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    saveFile = ("%s/%srd.mb" % (out_dir,filename[:-2]))
    cmds.file(rn=saveFile)
    cmds.file(f=True, s=True)
    logger.info(("%s Save Finally"% saveFile), exc_info=True)

    print (rencheck)
    print (mod)
    _render(rencheck,mod,filename,savefilepath)

# if __name__ == '__main__':
#     main()
