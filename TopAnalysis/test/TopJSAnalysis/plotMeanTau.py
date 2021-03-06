import ROOT
ROOT.gROOT.SetBatch(True)
import optparse
import os,sys
import json
import re
from collections import OrderedDict
from math import sqrt

debug = True

"""
steer the script
"""
def main():
    
    cmsLabel='#bf{CMS}'
    
    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option(     '--mcUnc',        dest='mcUnc'  ,      help='common MC related uncertainty (e.g. lumi)',        default=0,              type=float)
    parser.add_option(     '--com',          dest='com'  ,        help='center of mass energy',                            default='13 TeV',       type='string')
    parser.add_option('-j', '--json',        dest='json'  ,      help='json with list of files',        default='data/era2016/samples.json',              type='string')
    parser.add_option( '--systJson', dest='systJson', help='json with list of systematics', default='data/era2016/syst_samples.json', type='string')
    parser.add_option('-i', '--inDir',       dest='inDir' ,      help='input directory',                default='unfolding/result',              type='string')
    parser.add_option('-O', '--outDir',      dest='outDir' ,     help='output directory',                default='unfolding/result',              type='string')
    parser.add_option('-o', '--outName',     dest='outName' ,    help='name of the output file',        default='plotter.root',    type='string')
    parser.add_option(      '--silent',      dest='silent' ,     help='only dump to ROOT file',         default=False,             action='store_true')
    parser.add_option(      '--saveTeX',     dest='saveTeX' ,    help='save as tex file as well',       default=False,             action='store_true')
    parser.add_option('-l', '--lumi',        dest='lumi' ,       help='lumi [/pb]',              default=35922.,              type=float)
    parser.add_option('--obs', dest='obs',  default='mult', help='observable [default: %default]')
    parser.add_option('--flavor', dest='flavor',  default='all', help='flavor [default: %default]')
    (opt, args) = parser.parse_args()

    #read lists of samples
    staus = ['21', '32', '43']
    flavors = ['incl', 'bottom', 'light', 'gluon']
    colors = {'incl': ROOT.kBlack, 'bottom': ROOT.kRed+1, 'light': ROOT.kBlue+1, 'gluon': ROOT.kGreen+1}
    markers = {'incl': 20, 'bottom': 21, 'light': 22, 'gluon': 23}
    fills = {'incl': 1001, 'bottom': 3254, 'light': 3245, 'gluon': 3390}
    infiles = {}
    hists = {}
    unchists = {}
    
    dataUnfolded = ROOT.TH1F('dataUnfolded', 'dataUnfolded', 12, 0, 12)
    dataUnfoldedSys = ROOT.TH1F('dataUnfoldedSys', 'dataUnfoldedSys', 12, 0, 12)
    nominalGen = ROOT.TH1F('nominalGen', 'nominalGen', 12, 0, 12)
    FSRUpGen = ROOT.TH1F('FSRUpGen', 'FSRUpGen',       12, 0, 12)
    FSRDownGen = ROOT.TH1F('FSRDownGen', 'FSRDownGen', 12, 0, 12)
    herwigGen = ROOT.TH1F('herwigGen', 'herwigGen',    12, 0, 12)
    sherpaGen = ROOT.TH1F('sherpaGen', 'sherpaGen',    12, 0, 12)
    
    counter = 0
    for flavor in flavors:
        for stau in staus:
            counter += 1
            infile = ROOT.TFile.Open('%s/tau%s_charged_%s_result.root'%(opt.inDir, stau, flavor))
            
            inhist = infile.Get('mean')
            dataUnfolded.SetBinContent(counter, inhist.GetBinContent(1))
            dataUnfolded.SetBinError(counter, inhist.GetBinError(1))
            
            inhistErr = infile.Get('meanErr')
            dataUnfoldedSys.SetBinContent(counter, inhistErr.GetBinContent(1))
            dataUnfoldedSys.SetBinError(counter, inhistErr.GetBinError(1))
            dataUnfoldedSys.GetXaxis().SetBinLabel(counter, '#tau_{%s}'%(stau))
            
            innominalGen = infile.Get('nominalGen')
            nominalGen.SetBinContent(counter, innominalGen.GetMean())
            nominalGen.SetBinError(counter, innominalGen.GetMeanError())
            
            inFSRUpGen = infile.Get('FSRUpGen')
            FSRUpGen.SetBinContent(counter, inFSRUpGen.GetMean())
            FSRUpGen.SetBinError(counter, inFSRUpGen.GetMeanError())
            
            inFSRDownGen = infile.Get('FSRDownGen')
            FSRDownGen.SetBinContent(counter, inFSRDownGen.GetMean())
            FSRDownGen.SetBinError(counter, inFSRDownGen.GetMeanError())
            
            inHerwigGen = infile.Get('herwigGen')
            herwigGen.SetBinContent(counter, inHerwigGen.GetMean())
            herwigGen.SetBinError(counter, inHerwigGen.GetMeanError())
            
            inSherpaGen = infile.Get('sherpaGen')
            sherpaGen.SetBinContent(counter, inSherpaGen.GetMean())
            sherpaGen.SetBinError(counter, inSherpaGen.GetMeanError())
    
    #plot
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas('c','c',500,500)
    c.SetBottomMargin(0.0)
    c.SetLeftMargin(0.0)
    c.SetTopMargin(0)
    c.SetRightMargin(0.00)
    c.cd()
    
    p1=ROOT.TPad('p1','p1',0.0,0.2,1.0,1.0)
    p1.SetRightMargin(0.05)
    p1.SetLeftMargin(0.12)
    p1.SetTopMargin(0.06)
    p1.SetBottomMargin(0.01)
    p1.Draw()
    p1.cd()
    
    dataUnfolded.SetTitle('')
    dataUnfolded.SetXTitle('')
    dataUnfolded.GetXaxis().SetTitleSize(0.045)
    dataUnfolded.GetXaxis().SetLabelSize(0.04)
    dataUnfolded.SetYTitle('<#tau_{NM}>')
    dataUnfolded.GetYaxis().SetRangeUser(0.48, 0.74)
    dataUnfolded.GetYaxis().SetTitleSize(0.05)
    dataUnfolded.GetYaxis().SetLabelSize(0.045)
    dataUnfolded.GetYaxis().SetTitleOffset(1.1)
    dataUnfolded.SetLineColor(ROOT.kBlack)
    dataUnfolded.SetMarkerColor(ROOT.kBlack)
    dataUnfolded.SetMarkerStyle(20)
    dataUnfolded.Draw('P X0 E1')
    
    dataUnfoldedSys.SetLineWidth(2)
    dataUnfoldedSys.SetLineColor(ROOT.kBlack)
    dataUnfoldedSys.SetMarkerColor(ROOT.kBlack)
    dataUnfoldedSys.SetMarkerStyle(1)
    dataUnfoldedSys.Draw('SAME P X0 E1')
    
    dataUnfolded.SetLineColor(ROOT.kBlack)
    dataUnfolded.SetMarkerColor(ROOT.kBlack)
    dataUnfolded.SetMarkerStyle(20)
    dataUnfolded.Draw('SAME P X0 E1')
    
    nominalGen.SetLineColor(ROOT.kRed+1)
    nominalGen.SetLineWidth(2)
    nominalGen.SetMarkerColor(ROOT.kRed+1)
    nominalGen.SetMarkerStyle(24)
    nominalGen.Draw('SAME H')
    
    FSRUpGen.SetLineColor(ROOT.kRed+1)
    FSRUpGen.SetMarkerColor(ROOT.kRed+1)
    FSRUpGen.SetMarkerStyle(26)
    FSRUpGen.Draw('SAME P X0 E1')
    
    FSRDownGen.SetLineColor(ROOT.kRed+1)
    FSRDownGen.SetMarkerColor(ROOT.kRed+1)
    FSRDownGen.SetMarkerStyle(32)
    FSRDownGen.Draw('SAME P X0 E1')
    
    herwigGen.SetLineColor(ROOT.kBlue+1)
    herwigGen.SetLineStyle(7)
    herwigGen.SetLineWidth(2)
    herwigGen.SetMarkerColor(ROOT.kBlue+1)
    herwigGen.SetMarkerStyle(25)
    herwigGen.Draw('SAME H')
    
    sherpaGen.SetLineColor(ROOT.kGreen+2)
    sherpaGen.SetLineStyle(5)
    sherpaGen.SetLineWidth(2)
    sherpaGen.SetMarkerColor(ROOT.kGreen+2)
    sherpaGen.SetMarkerStyle(27)
    sherpaGen.Draw('SAME H')
    
    inix = 0.5
    if (nominalGen.GetMaximumBin() > nominalGen.GetNbinsX()/2.): inix = 0.15
    legend = ROOT.TLegend(inix,0.55,inix+0.45,0.9)
    legend.SetLineWidth(0)
    legend.SetFillStyle(0)
    dummy = dataUnfolded.Clone('dummy')
    dummy.SetMarkerSize(0)
    legend.AddEntry(dataUnfolded, "Data", "ep")
    legend.AddEntry(nominalGen, "Powheg+Pythia 8", "pl")
    dummy1 = legend.AddEntry(dummy, "(#alpha_{s}^{FSR}(m_{Z})=0.1365, with MEC)", "p")
    dummy1.SetTextSize(0.0225)
    dummy1.SetTextAlign(13)
    legend.AddEntry(FSRUpGen, "#minus FSR up  #scale[0.65]{(#alpha_{s}^{FSR}(m_{Z})=0.1543)}", "p")
    legend.AddEntry(FSRDownGen, "#minus FSR down  #scale[0.65]{(#alpha_{s}^{FSR}(m_{Z})=0.1224)}", "p")
    #legend.AddEntry(qcdBasedGen, "#minus QCD-based CR", "p")
    legend.AddEntry(herwigGen, "Powheg+Herwig 7", "pl")
    dummy2 = legend.AddEntry(dummy, "(#alpha_{s}^{FSR}(m_{Z}) = 0.126234, with MEC)", "p")
    dummy2.SetTextSize(0.0225)
    dummy2.SetTextAlign(13)
    legend.AddEntry(sherpaGen, "Sherpa", "pl")
    dummy3 = legend.AddEntry(dummy, "(#alpha_{s}^{FSR}(m_{Z}) = 0.118, no MEC)", "p")
    dummy3.SetTextSize(0.0225)
    dummy3.SetTextAlign(13)
    legend.Draw()
    txt=ROOT.TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(42)
    txt.SetTextSize(0.05)
    txt.SetTextAlign(12)
    inix = 0.15
    if (nominalGen.GetMaximumBin() > nominalGen.GetNbinsX()/2.): inix = 0.83
    txt.DrawLatex(inix,0.88,cmsLabel)
    txt.DrawLatex(0.7,0.97,'#scale[0.8]{%3.1f fb^{-1} (%s)}' % (opt.lumi/1000.,opt.com) )
    
    lineHeight = 0.63
    txt.DrawLatex(0.175,0.05,'incl jets')
    divider1 = ROOT.TLine(3, 0., 3, lineHeight)
    divider1.SetLineColor(ROOT.kBlack)
    divider1.Draw()
    txt.DrawLatex(0.375,0.05,'bottom')
    divider2 = ROOT.TLine(6, 0., 6, lineHeight)
    divider2.SetLineColor(ROOT.kBlack)
    divider2.Draw()
    txt.DrawLatex(0.6,0.10,'light')
    txt.DrawLatex(0.57,0.05,'enriched')
    divider4 = ROOT.TLine(9, 0., 9, lineHeight)
    divider4.SetLineColor(ROOT.kBlack)
    divider4.Draw()
    txt.DrawLatex(0.8,0.10,'gluon')
    txt.DrawLatex(0.775,0.05,'enriched')
    
    c.cd()
    p2 = ROOT.TPad('p2','p2',0.0,0.0,1.0,0.2)
    p2.Draw()
    p2.SetBottomMargin(0.4)
    p2.SetRightMargin(0.05)
    p2.SetLeftMargin(0.12)
    p2.SetTopMargin(0.01)
    p2.cd()
    
    dataUnfoldedRatio=dataUnfolded.Clone('dataUnfoldedRatio')
    dataUnfoldedRatio.Divide(dataUnfolded)
    dataUnfoldedRatio.SetFillStyle(3254)
    dataUnfoldedRatio.SetFillColor(ROOT.kBlack)
    
    dataUnfoldedSysRatio=dataUnfoldedSys.Clone('dataUnfoldedSysRatio')
    dataUnfoldedSysRatio.Divide(dataUnfolded)
    dataUnfoldedSysRatio.SetTitle('')
    dataUnfoldedSysRatio.SetXTitle(dataUnfolded.GetXaxis().GetTitle())
    dataUnfoldedSysRatio.SetYTitle('MC/data')
    dataUnfoldedSysRatio.SetFillColor(ROOT.kGray)
    dataUnfoldedSysRatio.GetXaxis().SetTitleSize(0.2)
    dataUnfoldedSysRatio.GetXaxis().SetTitleOffset(0.8)
    dataUnfoldedSysRatio.GetXaxis().SetLabelSize(0.275)
    dataUnfoldedSysRatio.GetXaxis().SetLabelOffset(0.05)
    dataUnfoldedSysRatio.GetYaxis().SetTitleSize(0.2)
    dataUnfoldedSysRatio.GetYaxis().SetTitleOffset(0.3)
    dataUnfoldedSysRatio.GetYaxis().SetLabelSize(0.18)
    dataUnfoldedSysRatio.GetYaxis().SetRangeUser(0.96,1.11)
    dataUnfoldedSysRatio.GetYaxis().SetNdivisions(503)
    
    nominalGenRatio=nominalGen.Clone('nominalGenRatio')
    nominalGenRatio.Divide(dataUnfolded)
    FSRUpGenRatio=FSRUpGen.Clone('FSRUpGenRatio')
    FSRUpGenRatio.Divide(dataUnfolded)
    FSRDownGenRatio=FSRDownGen.Clone('FSRDownGenRatio')
    FSRDownGenRatio.Divide(dataUnfolded)
    herwigGenRatio=herwigGen.Clone('herwigGenRatio')
    herwigGenRatio.Divide(dataUnfolded)
    sherpaGenRatio=sherpaGen.Clone('sherpaGenRatio')
    sherpaGenRatio.Divide(dataUnfolded)
    
    dataUnfoldedSysRatio.SetMarkerStyle(0)
    dataUnfoldedSysRatio.Draw('e2')
    dataUnfoldedRatio.SetMarkerStyle(0)
    dataUnfoldedRatio.Draw('e2,same')
    line = dataUnfoldedSysRatio.Clone('line')
    line.SetLineColor(ROOT.kBlack)
    line.SetFillStyle(0)
    for i in range(line.GetNbinsX()+2): line.SetBinContent(i, 1.)
    line.Draw('hist same')
    
    nominalGenRatio.Draw('SAME H')
    FSRUpGenRatio.Draw  ('SAME P X0 E1')
    FSRDownGenRatio.Draw('SAME P X0 E1')
    herwigGenRatio.Draw ('SAME H')
    sherpaGenRatio.Draw ('SAME H')
    
    lineStart = 0.94
    lineHeight = 2.
    ratio_divider1 = ROOT.TLine(3, lineStart, 3, lineHeight)
    ratio_divider1.SetLineColor(ROOT.kBlack)
    ratio_divider1.Draw()
    ratio_divider2 = ROOT.TLine(6, lineStart, 6, lineHeight)
    ratio_divider2.SetLineColor(ROOT.kBlack)
    ratio_divider2.Draw()
    ratio_divider4 = ROOT.TLine(9, lineStart, 9, lineHeight)
    ratio_divider4.SetLineColor(ROOT.kBlack)
    ratio_divider4.Draw()
            
    c.Print(opt.outDir+'/meanTau.pdf')
    c.Print(opt.outDir+'/meanTau.png')
        
def normalizeAndDivideByBinWidth(hist):
    hist.Scale(1./hist.Integral())
    for i in range(1, hist.GetNbinsX()+1):
        hist.SetBinContent(i, hist.GetBinContent(i)/hist.GetBinWidth(i))
        hist.SetBinError  (i, hist.GetBinError(i)  /hist.GetBinWidth(i))
    return hist

"""
for execution from another script
"""
if __name__ == "__main__":
    main()
    #sys.exit(main())

