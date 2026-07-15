from Configurables import ApplicationMgr
from Gaudi.Configuration import *
from Configurables import LcioEvent, EventDataSvc, MarlinProcessorWrapper
from k4MarlinWrapper.parseConstants import *
import glob
import json
import os

def load_ddmarlin_parameter_payload(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected dict payload in {path}")
    normalized = {}
    for key, values in payload.items():
        if not isinstance(values, list):
            raise RuntimeError(f"Expected list value for DDMarlin parameter '{key}' in {path}")
        normalized[key] = [str(value) for value in values]
    return normalized

from k4FWCore.parseArgs import parser

parser.add_argument("--enableBIB", action="store_true", default=False, help="Enable BIB overlay")
parser.add_argument("--enableIP", action="store_true", default=False, help="Enable IP overlay")
parser.add_argument("--TypeEvent", type=str, default="pions_0_50", help="Type of event to process")
parser.add_argument("--InFileName", type=str, default="0", help="Input file name for the simulation")
parser.add_argument("--code", type=str, default="/scratch/jwatts/mucol/v2.11", help="Top-level directory for code")
parser.add_argument("--data", type=str, default="/dataMuC", help="Top-level directory for data")
parser.add_argument("--compressionLevel", type=int, default=None, help="Set compression level of output")
parser.add_argument("--overlayMixNumberBackground", type=int, default=1666, help="Number of background files for OverlayMix")
parser.add_argument("--skipReco", action="store_true", default=False, help="Skip reconstruction")
parser.add_argument("--skipTrackerConing", action="store_true", default=False, help="Skip tracker coning")
parser.add_argument("--inputFile", type=str, default="", help="Input file, if set ignores the automatic path lookup in `--data`")
parser.add_argument("--outputFile", type=str, default="", help="Output file, if set ignores the automatic output path generation in `--data`")
parser.add_argument("--useLocalThresholds", action="store_true", default=False, help="Read MyBIBUtils thresholds files from code directory, rather than from the container")
#parser.add_argument("--photonEMCalibPayload", type=str, default=None, help="JSON payload for Pandora EM theta-energy correction")
#parser.add_argument("--hadronicCalibPayload", type=str, default=None, help="JSON payload for Pandora HAD theta-energy correction")
the_args = parser.parse_args()

Coned = "" if the_args.skipTrackerConing else "Coned"

algList = []
evtsvc = EventDataSvc()

CONSTANTS = {
}

parseConstants(CONSTANTS)

read = LcioEvent()
read.OutputLevel = INFO
if the_args.inputFile == "":
    read.Files = [f"/scratch/jwatts/mucol/v2.11/sim/photonGun_transitionRegion_1000_5000_sim_0.slcio"]
else:
    read.Files = [the_args.inputFile]
algList.append(read)

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = INFO
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
    "HowOften": ["1"]
}

MyAIDAProcessor = MarlinProcessorWrapper("MyAIDAProcessor")
MyAIDAProcessor.OutputLevel = INFO
MyAIDAProcessor.ProcessorType = "AIDAProcessor"
MyAIDAProcessor.Parameters = {
    "FileName": ["lctuple_photons_0_50_actsseededckf"],
    "FileType": ["root"]
}

Output_REC = MarlinProcessorWrapper("Output_REC")
Output_REC.OutputLevel = INFO
Output_REC.ProcessorType = "LCIOOutputProcessor"
if not the_args.enableBIB:
    Output_REC.Parameters = {
        "DropCollectionTypes": [],
        "DropCollectionNames": [],
        "FullSubsetCollections": [],
        "KeepCollectionNames": ["MCParticle_SiTracks", "MCParticle_SelectedTracks"],
        "LCIOOutputFile": [the_args.outputFile if the_args.outputFile != "" else "/scratch/jwatts/mucol/v2.11/reco/photonGun_transitionRegion_1000_5000_reco_0.slcio"],
        "LCIOWriteMode": ["WRITE_NEW"]
    }
else:
    Output_REC.Parameters = {
        "DropCollectionTypes": [
            "SimTrackerHit",
            "SimCalorimeterHit",
            "CalorimeterHit",
            "TrackerHitPlane",
            "LCRelation"
        ],
        "DropCollectionNames": [
            "AllTracks", "SeedTracks", "SiTracks_Refitted",
            "MCPhysicsParticles", "MCPhysicsParticles_IP"
        ],
        "FullSubsetCollections": [
            "EcalBarrelCollectionSel", "EcalEndcapCollectionSel",
            "HcalBarrelCollectionSel", "HcalEndcapCollectionSel",
            f"IBTrackerHits{Coned}", f"IETrackerHits{Coned}",
            f"OBTrackerHits{Coned}", f"OETrackerHits{Coned}",
            f"VBTrackerHits{Coned}", f"VETrackerHits{Coned}",
            f"VBTrackerHitsRelations{Coned}", f"VETrackerHitsRelations{Coned}",
            f"IBTrackerHitsRelations{Coned}", f"IETrackerHitsRelations{Coned}",
            f"OBTrackerHitsRelations{Coned}", f"OETrackerHitsRelations{Coned}",
            f"VertexBarrelCollection{Coned}", f"VertexEndcapCollection{Coned}",
            f"InnerTrackerBarrelCollection{Coned}", f"InnerTrackerEndcapCollection{Coned}",
            f"OuterTrackerBarrelCollection{Coned}", f"OuterTrackerEndcapCollection{Coned}",
            "SiTracks", "SelectedTracks"
        ],
        "KeepCollectionNames": [
            "EcalBarrelCollectionSel", "EcalEndcapCollectionSel",
            "HcalBarrelCollectionSel", "HcalEndcapCollectionSel",
            f"IBTrackerHits{Coned}", f"IETrackerHits{Coned}",
            f"OBTrackerHits{Coned}", f"OETrackerHits{Coned}",
            f"VBTrackerHits{Coned}", f"VETrackerHits{Coned}",
            f"VBTrackerHitsRelations{Coned}", f"VETrackerHitsRelations{Coned}",
            f"IBTrackerHitsRelations{Coned}", f"IETrackerHitsRelations{Coned}",
            f"OBTrackerHitsRelations{Coned}", f"OETrackerHitsRelations{Coned}",
            f"VertexBarrelCollection{Coned}", f"VertexEndcapCollection{Coned}",
            f"InnerTrackerBarrelCollection{Coned}", f"InnerTrackerEndcapCollection{Coned}",
            f"OuterTrackerBarrelCollection{Coned}", f"OuterTrackerEndcapCollection{Coned}",
            "SiTracks", "SelectedTracks",
            "MCParticle_SiTracks", "MCParticle_SelectedTracks"
        ],
        "LCIOOutputFile": [the_args.outputFile if the_args.outputFile != "" else "/scratch/jwatts/mucol/v2.11/reco/photonGun_transitionRegion_1000_5000_reco_0.slcio"],
        "LCIOWriteMode": ["WRITE_NEW"]
    }

if the_args.compressionLevel is not None:
    Output_REC.Parameters["CompressionLevel"] = [str(the_args.compressionLevel)]

InitDD4hep = MarlinProcessorWrapper("InitDD4hep")
InitDD4hep.OutputLevel = INFO
InitDD4hep.ProcessorType = "InitializeDD4hep"
InitDD4hep.Parameters = {
    "DD4hepXMLFile": [os.environ['k4geo_DIR']+"/MuColl/MAIA/compact/MAIA_v0/MAIA_v0.xml"],
    "EncodingStringParameterName": ["GlobalTrackerReadoutID"]
}

VXDBarrelDigitiser = MarlinProcessorWrapper("VXDBarrelDigitiser")
VXDBarrelDigitiser.OutputLevel = INFO
VXDBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDBarrelDigitiser.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.03"],
    "ResolutionU": ["0.005"],
    "ResolutionV": ["0.005"],
    "SimTrackHitCollectionName": ["VertexBarrelCollection"],
    "SimTrkHitRelCollection": ["VBTrackerHitsRelations"],
    "SubDetectorName": ["Vertex"],
    "TimeWindowMax": ["0.15"],
    "TimeWindowMin": ["-0.09"],
    "TrackerHitCollectionName": ["VBTrackerHits"],
    "UseTimeWindow": ["true"]
}

VXDEndcapDigitiser = MarlinProcessorWrapper("VXDEndcapDigitiser")
VXDEndcapDigitiser.OutputLevel = INFO
VXDEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDEndcapDigitiser.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.03"],
    "ResolutionU": ["0.005"],
    "ResolutionV": ["0.005"],
    "SimTrackHitCollectionName": ["VertexEndcapCollection"],
    "SimTrkHitRelCollection": ["VETrackerHitsRelations"],
    "SubDetectorName": ["Vertex"],
    "TimeWindowMax": ["0.15"],
    "TimeWindowMin": ["-0.09"],
    "TrackerHitCollectionName": ["VETrackerHits"],
    "UseTimeWindow": ["true"]
}

InnerPlanarDigiProcessor = MarlinProcessorWrapper("InnerPlanarDigiProcessor")
InnerPlanarDigiProcessor.OutputLevel = INFO
InnerPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["InnerTrackerBarrelCollection"],
    "SimTrkHitRelCollection": ["IBTrackerHitsRelations"],
    "SubDetectorName": ["InnerTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["IBTrackerHits"],
    "UseTimeWindow": ["true"]
}

InnerEndcapPlanarDigiProcessor = MarlinProcessorWrapper(
    "InnerEndcapPlanarDigiProcessor")
InnerEndcapPlanarDigiProcessor.OutputLevel = INFO
InnerEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerEndcapPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["InnerTrackerEndcapCollection"],
    "SimTrkHitRelCollection": ["IETrackerHitsRelations"],
    "SubDetectorName": ["InnerTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["IETrackerHits"],
    "UseTimeWindow": ["true"]
}

OuterPlanarDigiProcessor = MarlinProcessorWrapper("OuterPlanarDigiProcessor")
OuterPlanarDigiProcessor.OutputLevel = INFO
OuterPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["OuterTrackerBarrelCollection"],
    "SimTrkHitRelCollection": ["OBTrackerHitsRelations"],
    "SubDetectorName": ["OuterTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["OBTrackerHits"],
    "UseTimeWindow": ["true"]
}

OuterEndcapPlanarDigiProcessor = MarlinProcessorWrapper(
    "OuterEndcapPlanarDigiProcessor")
OuterEndcapPlanarDigiProcessor.OutputLevel = INFO
OuterEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterEndcapPlanarDigiProcessor.Parameters = {
    "CorrectTimesForPropagation": ["true"],
    "IsStrip": ["false"],
    "ResolutionT": ["0.06"],
    "ResolutionU": ["0.007"],
    "ResolutionV": ["0.090"],
    "SimTrackHitCollectionName": ["OuterTrackerEndcapCollection"],
    "SimTrkHitRelCollection": ["OETrackerHitsRelations"],
    "SubDetectorName": ["OuterTrackers"],
    "TimeWindowMax": ["0.3"],
    "TimeWindowMin": ["-0.18"],
    "TrackerHitCollectionName": ["OETrackerHits"],
    "UseTimeWindow": ["true"]
}

VXDBarrelConer = MarlinProcessorWrapper("VXDBarrelConer")
VXDBarrelConer.OutputLevel = INFO
VXDBarrelConer.ProcessorType = "FilterConeHits"
VXDBarrelConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["VBTrackerHits"],
    "TrackerSimHitInputCollections": ["VertexBarrelCollection"],
    "TrackerHitInputRelations": ["VBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["VBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["VertexBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["VBTrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

VXDEndcapConer = MarlinProcessorWrapper("VXDEndcapConer")
VXDEndcapConer.OutputLevel = INFO
VXDEndcapConer.ProcessorType = "FilterConeHits"
VXDEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["VETrackerHits"],
    "TrackerSimHitInputCollections": ["VertexEndcapCollection"],
    "TrackerHitInputRelations": ["VETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["VETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["VertexEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["VETrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

InnerPlanarConer = MarlinProcessorWrapper("InnerPlanarConer")
InnerPlanarConer.OutputLevel = INFO
InnerPlanarConer.ProcessorType = "FilterConeHits"
InnerPlanarConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["IBTrackerHits"],
    "TrackerSimHitInputCollections": ["InnerTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["IBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["IBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["InnerTrackerBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["IBTrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

InnerEndcapConer = MarlinProcessorWrapper("InnerEndcapConer")
InnerEndcapConer.OutputLevel = INFO
InnerEndcapConer.ProcessorType = "FilterConeHits"
InnerEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["IETrackerHits"],
    "TrackerSimHitInputCollections": ["InnerTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["IETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["IETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["InnerTrackerEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["IETrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

OuterPlanarConer = MarlinProcessorWrapper("OuterPlanarConer")
OuterPlanarConer.OutputLevel = INFO
OuterPlanarConer.ProcessorType = "FilterConeHits"
OuterPlanarConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["OBTrackerHits"],
    "TrackerSimHitInputCollections": ["OuterTrackerBarrelCollection"],
    "TrackerHitInputRelations": ["OBTrackerHitsRelations"],
    "TrackerHitOutputCollections": ["OBTrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["OuterTrackerBarrelCollectionConed"],
    "TrackerHitOutputRelations": ["OBTrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

OuterEndcapConer = MarlinProcessorWrapper("OuterEndcapConer")
OuterEndcapConer.OutputLevel = INFO
OuterEndcapConer.ProcessorType = "FilterConeHits"
OuterEndcapConer.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "TrackerHitInputCollections": ["OETrackerHits"],
    "TrackerSimHitInputCollections": ["OuterTrackerEndcapCollection"],
    "TrackerHitInputRelations": ["OETrackerHitsRelations"],
    "TrackerHitOutputCollections": ["OETrackerHitsConed"],
    "TrackerSimHitOutputCollections": ["OuterTrackerEndcapCollectionConed"],
    "TrackerHitOutputRelations": ["OETrackerHitsRelationsConed"],
    "Dist3DCut": ["30."],
    "FillHistograms": ["false"]
}

CKFTracking = MarlinProcessorWrapper("CKFTracking")
CKFTracking.OutputLevel = INFO
CKFTracking.ProcessorType = "ACTSSeededCKFTrackingProc"
CKFTracking.Parameters = {
    "CKF_Chi2CutOff": ["10"],
    "CKF_NumMeasurementsCutOff": ["1"],
    "CaloFace_Radius": ["1857"],
    "CaloFace_Z": ["2307"],
    "MatFile": [os.environ['ACTSTRACKING_DATA']+"/MAIA_v0_material.json"],
    "PropagateBackward": ["False"],
    "DetectorSchema": ["MAIA_v0"],
    "RunCKF": ["True"],
    "SeedFinding_CollisionRegion": ["6"],
    "SeedFinding_ImpactMax": ["3"],
    "SeedFinding_MinPt": ["500"],
    "SeedFinding_RMax": ["150"],
    "SeedFinding_ZMax": ["600"],
    "SeedFinding_RadLengthPerSeed": ["0.1"],
    "SeedFinding_SigmaScattering": ["50"],
    "SeedingLayers": ["13", "2", "13", "6", "13", "10", "13", "14",
                      "14", "2", "14", "6", "14", "8", "14", "10",
                      "15", "2", "15", "6", "15", "10", "15", "14",
                      "8", "2",
                      "17", "2",
                      "18", "2"],
    "TGeoFile": [os.environ['ACTSTRACKING_DATA']+"/MAIA_v0.root"],
    "TGeoDescFile": [os.environ['ACTSTRACKING_DATA']+"/MAIA_v0.json"],
    "TrackCollectionName": ["AllTracks"],
    "TrackerHitCollectionNames": [f"VBTrackerHits{Coned}", f"IBTrackerHits{Coned}", f"OBTrackerHits{Coned}", f"VETrackerHits{Coned}", f"IETrackerHits{Coned}", f"OETrackerHits{Coned}"]
}

TrackDeduper = MarlinProcessorWrapper("TrackDeduper")
TrackDeduper.OutputLevel = INFO
TrackDeduper.ProcessorType = "ACTSDuplicateRemoval"
TrackDeduper.Parameters = {
    "InputTrackCollectionName": ["AllTracks"],
    "OutputTrackCollectionName": ["SiTracks"]
}

MyTrackTruth = MarlinProcessorWrapper("MyTrackTruth")
MyTrackTruth.OutputLevel = INFO
MyTrackTruth.ProcessorType = "TrackTruthProc"
MyTrackTruth.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "Particle2TrackRelationName": ["MCParticle_SiTracks"],
    "TrackCollection": ["SiTracks"],
    "TrackerHit2SimTrackerHitRelationName": [f"VBTrackerHitsRelations{Coned}", f"IBTrackerHitsRelations{Coned}", f"OBTrackerHitsRelations{Coned}", f"VETrackerHitsRelations{Coned}", f"IETrackerHitsRelations{Coned}", f"OETrackerHitsRelations{Coned}"]
}

MyTrackSelectorHoles = MarlinProcessorWrapper("MyTrackSelectorHoles")
MyTrackSelectorHoles.OutputLevel = ERROR
MyTrackSelectorHoles.ProcessorType = "FilterTracks"
MyTrackSelectorHoles.Parameters = {
    "InputTrackCollectionName": ["SiTracks"],
    "OutputTrackCollectionName": ["SiTracksPreFit"],
    "BarrelOnly": ["false"],
    "HasCaloState": ["false"],
    "NHitsTotal": ["8"],
    "NHitsVertex": ["0"],
    "NHitsInner": ["0"],
    "NHitsOuter": ["0"],
    "MinPt": ["0.5"],
    "MaxChi2OverNdf": ["5"],
    "MaxHoles": ["1"],
    "MaxD0": ["999"],
    "MaxZ0": ["999"]
}

Refit = MarlinProcessorWrapper("Refit")
Refit.OutputLevel = WARNING
Refit.ProcessorType = "RefitFinal"
Refit.Parameters = {
    "InputTrackCollectionName": ["SiTracksPreFit"],
    "InputRelationCollectionName": ["SiTrackRelations"],
    "OutputTrackCollectionName": ["SiTracks_Refitted"],
    "OutputRelationCollectionName": ["SiTracks_Refitted_Relation"],
    "MultipleScatteringOn": ["true"],
    "EnergyLossOn": ["true"],
    "SmoothOn": ["false"],
    "Max_Chi2_Incr": ["10."],
    "ReferencePoint": ["-1"],
    "extrapolateForward": ["true"],
    "MinClustersOnTrackAfterFit": ["3"],
    "MaxOutliersAllowed": ["2"],
    "ReducedChi2Cut": ["10."]
}

MyTrackSelector = MarlinProcessorWrapper("MyTrackSelector")
MyTrackSelector.OutputLevel = ERROR
MyTrackSelector.ProcessorType = "FilterTracks"
MyTrackSelector.Parameters = {
    "BarrelOnly": ["false"],
    "HasCaloState": ["true"],
    "NHitsTotal": ["8"],
    "NHitsVertex": ["0"],
    "NHitsInner": ["0"],
    "NHitsOuter": ["0"],
    "MinPt": ["0.5"],
    "MaxChi2OverNdf": ["3"],
    "MaxHoles": ["5"],
    "InputTrackCollectionName": ["SiTracks_Refitted"],
    "OutputTrackCollectionName": ["SelectedTracks"],
    "MaxD0": ["999"],
    "MaxZ0": ["999"]
}

MyTrackTruthSelected = MarlinProcessorWrapper("MyTrackTruthSelected")
MyTrackTruthSelected.OutputLevel = INFO
MyTrackTruthSelected.ProcessorType = "TrackTruthProc"
MyTrackTruthSelected.Parameters = {
    "MCParticleCollection": ["MCParticle"],
    "Particle2TrackRelationName": ["MCParticle_SelectedTracks"],
    "TrackCollection": ["SelectedTracks"],
    "TrackerHit2SimTrackerHitRelationName": [f"VBTrackerHitsRelations{Coned}", f"IBTrackerHitsRelations{Coned}", f"OBTrackerHitsRelations{Coned}", f"VETrackerHitsRelations{Coned}", f"IETrackerHitsRelations{Coned}", f"OETrackerHitsRelations{Coned}"]
}

MyEcalBarrelDigi = MarlinProcessorWrapper("MyEcalBarrelDigi")
MyEcalBarrelDigi.OutputLevel = INFO
MyEcalBarrelDigi.ProcessorType = "RealisticCaloDigiSilicon"
MyEcalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalBarrelCollection"],
    "outputHitCollections": ["EcalBarrelCollectionDigi"],
    "outputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10."],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

MyEcalBarrelReco = MarlinProcessorWrapper("MyEcalBarrelReco")
MyEcalBarrelReco.OutputLevel = INFO
MyEcalBarrelReco.ProcessorType = "RealisticCaloRecoSilicon"
MyEcalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0066150"],
    "calibration_layergroups": ["50"],
    "inputHitCollections": ["EcalBarrelCollectionDigi"],
    "inputRelationCollections": ["EcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["EcalBarrelCollectionRec"],
    "outputRelationCollections": ["EcalBarrelRelationsSimRec"]
}

MyEcalEndcapDigi = MarlinProcessorWrapper("MyEcalEndcapDigi")
MyEcalEndcapDigi.OutputLevel = INFO
MyEcalEndcapDigi.ProcessorType = "RealisticCaloDigiSilicon"
MyEcalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0001575"],
    "inputHitCollections": ["ECalEndcapCollection"],
    "outputHitCollections": ["EcalEndcapCollectionDigi"],
    "outputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "threshold": ["5e-05"],
    "thresholdUnit": ["GeV"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10."],
    "timingWindowMin": ["-0.5"],
    "elec_range_mip": ["15000"]
}

MyEcalEndcapReco = MarlinProcessorWrapper("MyEcalEndcapReco")
MyEcalEndcapReco.OutputLevel = INFO
MyEcalEndcapReco.ProcessorType = "RealisticCaloRecoSilicon"
MyEcalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.0066150"],
    "calibration_layergroups": ["50"],
    "inputHitCollections": ["EcalEndcapCollectionDigi"],
    "inputRelationCollections": ["EcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["EcalEndcapCollectionRec"],
    "outputRelationCollections": ["EcalEndcapRelationsSimRec"]
}

MyHcalBarrelDigi = MarlinProcessorWrapper("MyHcalBarrelDigi")
MyHcalBarrelDigi.OutputLevel = INFO
MyHcalBarrelDigi.ProcessorType = "RealisticCaloDigiScinPpd"
MyHcalBarrelDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalBarrelCollection"],
    "outputHitCollections": ["HcalBarrelCollectionDigi"],
    "outputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10."],
    "timingWindowMin": ["-0.5"]
}

MyHcalBarrelReco = MarlinProcessorWrapper("MyHcalBarrelReco")
MyHcalBarrelReco.OutputLevel = INFO
MyHcalBarrelReco.ProcessorType = "RealisticCaloRecoScinPpd"
MyHcalBarrelReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.024625"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalBarrelCollectionDigi"],
    "inputRelationCollections": ["HcalBarrelRelationsSimDigi"],
    "outputHitCollections": ["HcalBarrelCollectionRec"],
    "outputRelationCollections": ["HcalBarrelRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MyHcalEndcapDigi = MarlinProcessorWrapper("MyHcalEndcapDigi")
MyHcalEndcapDigi.OutputLevel = INFO
MyHcalEndcapDigi.ProcessorType = "RealisticCaloDigiScinPpd"
MyHcalEndcapDigi.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_mip": ["0.0004725"],
    "inputHitCollections": ["HCalEndcapCollection"],
    "outputHitCollections": ["HcalEndcapCollectionDigi"],
    "outputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"],
    "ppd_npix_uncert": ["0"],
    "ppd_pix_spread": ["0"],
    "threshold": ["0.5"],
    "thresholdUnit": ["MIP"],
    "timingCorrectForPropagation": ["1"],
    "timingCut": ["1"],
    "timingResolution": ["0"],
    "timingWindowMax": ["10."],
    "timingWindowMin": ["-0.5"]
}

MyHcalEndcapReco = MarlinProcessorWrapper("MyHcalEndcapReco")
MyHcalEndcapReco.OutputLevel = INFO
MyHcalEndcapReco.ProcessorType = "RealisticCaloRecoScinPpd"
MyHcalEndcapReco.Parameters = {
    "CellIDLayerString": ["layer"],
    "calibration_factorsMipGev": ["0.024625"],
    "calibration_layergroups": ["100"],
    "inputHitCollections": ["HcalEndcapCollectionDigi"],
    "inputRelationCollections": ["HcalEndcapRelationsSimDigi"],
    "outputHitCollections": ["HcalEndcapCollectionRec"],
    "outputRelationCollections": ["HcalEndcapRelationsSimRec"],
    "ppd_mipPe": ["15"],
    "ppd_npix": ["2000"]
}

MyEcalBarrelConer = MarlinProcessorWrapper("MyEcalBarrelConer")
MyEcalBarrelConer.OutputLevel = INFO
MyEcalBarrelConer.ProcessorType = "CaloConer"
MyEcalBarrelConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["EcalBarrelCollectionRec"],
    "CaloRelationCollectionName": ["EcalBarrelRelationsSimRec"],
    "GoodHitCollection": ["EcalBarrelCollectionConed"],
    "GoodRelationCollection": ["EcalBarrelRelationsSimConed"],
    "ConeWidth": ["0.6"]
}

MyEcalEndcapConer = MarlinProcessorWrapper("MyEcalEndcapConer")
MyEcalEndcapConer.OutputLevel = INFO
MyEcalEndcapConer.ProcessorType = "CaloConer"
MyEcalEndcapConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["EcalEndcapCollectionRec"],
    "CaloRelationCollectionName": ["EcalEndcapRelationsSimRec"],
    "GoodHitCollection": ["EcalEndcapCollectionConed"],
    "GoodRelationCollection": ["EcalEndcapRelationsSimConed"],
    "ConeWidth": ["0.6"]
}

MyHcalBarrelConer = MarlinProcessorWrapper("MyHcalBarrelConer")
MyHcalBarrelConer.OutputLevel = INFO
MyHcalBarrelConer.ProcessorType = "CaloConer"
MyHcalBarrelConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["HcalBarrelCollectionRec"],
    "CaloRelationCollectionName": ["HcalBarrelRelationsSimRec"],
    "GoodHitCollection": ["HcalBarrelCollectionConed"],
    "GoodRelationCollection": ["HcalBarrelRelationsSimConed"],
    "ConeWidth": ["0.6"]
}

MyHcalEndcapConer = MarlinProcessorWrapper("MyHcalEndcapConer")
MyHcalEndcapConer.OutputLevel = INFO
MyHcalEndcapConer.ProcessorType = "CaloConer"
MyHcalEndcapConer.Parameters = {
    "MCParticleCollectionName": ["MCParticle"],
    "CaloHitCollectionName": ["HcalEndcapCollectionRec"],
    "CaloRelationCollectionName": ["HcalEndcapRelationsSimRec"],
    "GoodHitCollection": ["HcalEndcapCollectionConed"],
    "GoodRelationCollection": ["HcalEndcapRelationsSimConed"],
    "ConeWidth": ["0.6"]
}

def findCaloThresholds(filename, codedir, use_code=False):
    if use_code:
        return os.path.join(codedir, filename)
    else:
        spack_root = os.path.commonpath([os.getenv("DD4HEP", ""), os.getenv("MUCOLL_STACK", "")])
        try:
            my_bib_utils = glob.glob(os.path.join(spack_root, "mybibutils*"))[0]
            return os.path.join(my_bib_utils, "share", filename)
        except IndexError:
            print("Could not find MyBIBUtils in spack installation, will try to read threshold files from --code.")
            return os.path.join(codedir, filename)

MyEcalBarrelSelector = MarlinProcessorWrapper("MyEcalBarrelSelector")
MyEcalBarrelSelector.OutputLevel = INFO
MyEcalBarrelSelector.ProcessorType = "CaloHitSelector"
MyEcalBarrelSelector.Parameters = {
    "CaloHitCollectionName": ["EcalBarrelCollectionConed"],
    "CaloRelationCollectionName": ["EcalBarrelRelationsSimConed"],
    "GoodHitCollection": ["EcalBarrelCollectionSel"],
    "GoodRelationCollection": ["EcalBarrelRelationsSimSel"],
    "ThresholdsFilePath": [findCaloThresholds("MyBIBUtils/data/ECAL_Thresholds_10TeV.root", the_args.code, the_args.useLocalThresholds)],
    "Nsigma": ["0"],
    "TimeWindowMin": ["-0.3"],
    "TimeWindowMax": ["0.3"],
    "DoBIBsubtraction": ["false"]
}

MyEcalEndcapSelector = MarlinProcessorWrapper("MyEcalEndcapSelector")
MyEcalEndcapSelector.OutputLevel = INFO
MyEcalEndcapSelector.ProcessorType = "CaloHitSelector"
MyEcalEndcapSelector.Parameters = {
    "CaloHitCollectionName": ["EcalEndcapCollectionConed"],
    "CaloRelationCollectionName": ["EcalEndcapRelationsSimConed"],
    "GoodHitCollection": ["EcalEndcapCollectionSel"],
    "GoodRelationCollection": ["EcalEndcapRelationsSimSel"],
    "ThresholdsFilePath": [findCaloThresholds("MyBIBUtils/data/ECAL_Thresholds_10TeV.root", the_args.code, the_args.useLocalThresholds)],
    "Nsigma": ["0"],
    "TimeWindowMin": ["-0.3"],
    "TimeWindowMax": ["0.3"],
    "DoBIBsubtraction": ["false"]
}

MyHcalBarrelSelector = MarlinProcessorWrapper("MyHcalBarrelSelector")
MyHcalBarrelSelector.OutputLevel = INFO
MyHcalBarrelSelector.ProcessorType = "CaloHitSelector"
MyHcalBarrelSelector.Parameters = {
    "CaloHitCollectionName": ["HcalBarrelCollectionConed"],
    "CaloRelationCollectionName": ["HcalBarrelRelationsSimConed"],
    "GoodHitCollection": ["HcalBarrelCollectionSel"],
    "GoodRelationCollection": ["HcalBarrelRelationsSimSel"],
    "ThresholdsFilePath": [findCaloThresholds("MyBIBUtils/data/HCAL_Thresholds_10TeV.root", the_args.code, the_args.useLocalThresholds)],
    "FlatThreshold": ["5e-05"],
    "Nsigma": ["0"],
    "TimeWindowMin": ["-0.3"],
    "TimeWindowMax": ["0.3"],
    "DoBIBsubtraction": ["false"]
}

MyHcalEndcapSelector = MarlinProcessorWrapper("MyHcalEndcapSelector")
MyHcalEndcapSelector.OutputLevel = INFO
MyHcalEndcapSelector.ProcessorType = "CaloHitSelector"
MyHcalEndcapSelector.Parameters = {
    "CaloHitCollectionName": ["HcalEndcapCollectionConed"],
    "CaloRelationCollectionName": ["HcalEndcapRelationsSimConed"],
    "GoodHitCollection": ["HcalEndcapCollectionSel"],
    "GoodRelationCollection": ["HcalEndcapRelationsSimSel"],
    "ThresholdsFilePath": [findCaloThresholds("MyBIBUtils/data/HCAL_Thresholds_10TeV.root", the_args.code, the_args.useLocalThresholds)],
    "FlatThreshold": ["5e-05"],
    "Nsigma": ["0"],
    "TimeWindowMin": ["-0.3"],
    "TimeWindowMax": ["0.3"],
    "DoBIBsubtraction": ["false"]
}

def updatePandoraPaths(pandoraSettings, codedir):
    newpath = os.path.join(os.path.dirname(pandoraSettings), "temp_" + os.path.basename(pandoraSettings))
    with open(pandoraSettings) as settingsFile:
        text = settingsFile.read()
    newtext = text.replace("/code", codedir)
    with open(newpath, 'w') as newSettings:
        newSettings.write(newtext)
    return newpath

pandoraSettingsFile = updatePandoraPaths(f"{the_args.code}/SteeringMacros/PandoraSettings/PandoraSettingsDefault.xml", the_args.code)
print("Running using temporary PandoraSettings XML: " + pandoraSettingsFile)

DDMarlinPandora = MarlinProcessorWrapper("DDMarlinPandora")
DDMarlinPandora.OutputLevel = INFO
DDMarlinPandora.ProcessorType = "DDPandoraPFANewProcessor"
DDMarlinPandora.Parameters = {
    "ClusterCollectionName": ["PandoraClusters"],
    "CreateGaps": ["false"],
    "CurvatureToMomentumFactor": ["0.00015"],
    "D0TrackCut": ["200"],
    "D0UnmatchedVertexTrackCut": ["5"],
    "DigitalMuonHits": ["0"],
    "ECalBarrelNormalVector": ["0", "0", "1"],
    "ECalCaloHitCollections": ["EcalBarrelCollectionSel", "EcalEndcapCollectionSel"],
    "ECalMipThreshold": ["0.5"],
    "ECalScMipThreshold": ["0"],
    "ECalScToEMGeVCalibration": ["1"],
    "ECalScToHadGeVCalibrationBarrel": ["1"],
    "ECalScToHadGeVCalibrationEndCap": ["1"],
    "ECalScToMipCalibration": ["1"],
    "ECalSiMipThreshold": ["0"],
    "ECalSiToEMGeVCalibration": ["1"],
    "ECalSiToHadGeVCalibrationBarrel": ["1"],
    "ECalSiToHadGeVCalibrationEndCap": ["1"],
    "ECalSiToMipCalibration": ["1"],
    "ECalToEMGeVCalibration": ["1.02373335516"],
    "ECalToHadGeVCalibrationBarrel": ["1.38"],
    "ECalToHadGeVCalibrationEndCap": ["1.38"],
    "ECalToMipCalibration": ["181.818"],
    "EMConstantTerm": ["0.01"],
    "EMStochasticTerm": ["0.17"],
    "FinalEnergyDensityBin": ["110."],
    "HCalBarrelNormalVector": ["0", "0", "1"],
    "HCalCaloHitCollections": ["HcalBarrelCollectionSel", "HcalEndcapCollectionSel"],
    "HCalMipThreshold": ["0.3"],
    "HCalToEMGeVCalibration": ["1.02373335516"],
    "HCalToHadGeVCalibration": ["1.25"],
    "HCalToMipCalibration": ["40.8163"],
    "HadConstantTerm": ["0.03"],
    "HadStochasticTerm": ["0.6"],
    "InputEnergyCorrectionPoints": [],
    "OutputEnergyCorrectionPoints": [],
    "KinkVertexCollections": ["KinkVertices"],
    "LayersFromEdgeMaxRearDistance": ["250"],
    "MCParticleCollections": ["MCParticle"],
    "MaxBarrelTrackerInnerRDistance": ["200"],
    "MaxClusterEnergyToApplySoftComp": ["0."],
    "MaxHCalHitHadronicEnergy": ["1000000"],
    "MaxTrackHits": ["5000"],
    "MaxTrackSigmaPOverP": ["0.15"],
    "MinBarrelTrackerHitFractionOfExpected": ["0"],
    "MinCleanCorrectedHitEnergy": ["0.1"],
    "MinCleanHitEnergy": ["0.5"],
    "MinCleanHitEnergyFraction": ["0.01"],
    "MinFtdHitsForBarrelTrackerHitFraction": ["0"],
    "MinFtdTrackHits": ["0"],
    "MinMomentumForTrackHitChecks": ["0"],
    "MinTpcHitFractionOfExpected": ["0"],
    "MinTrackECalDistanceFromIp": ["0"],
    "MinTrackHits": ["0"],
    "MuonBarrelBField": ["0.0001"],
    "MuonCaloHitCollections": ["MUON"],
    "MuonEndCapBField": ["0.0001"],
    "MuonHitEnergy": ["0.5"],
    "MuonToMipCalibration": ["19607.8"],
    "NEventsToSkip": ["0"],
    "NOuterSamplingLayers": ["3"],
    "PFOCollectionName": ["PandoraPFOs"],
    "PandoraSettingsXmlFile": [pandoraSettingsFile],
    "ProngVertexCollections": ["ProngVertices"],
    "ReachesECalBarrelTrackerOuterDistance": ["-100"],
    "ReachesECalBarrelTrackerZMaxDistance": ["-50"],
    "ReachesECalFtdZMaxDistance": ["1"],
    "ReachesECalMinFtdLayer": ["0"],
    "ReachesECalNBarrelTrackerHits": ["0"],
    "ReachesECalNFtdHits": ["0"],
    "RelCaloHitCollections": ["EcalBarrelRelationsSimSel", "EcalEndcapRelationsSimSel", "HcalBarrelRelationsSimSel", "HcalEndcapRelationsSimSel", "RelationMuonHit"],
    "RelTrackCollections": ["SelectedTracks_Relation"],
    "ShouldFormTrackRelationships": ["1"],
    "SoftwareCompensationEnergyDensityBins": ["0", "2.", "5.", "7.5", "9.5", "13.", "16.", "20.", "23.5", "28.", "33.", "40.", "50.", "75.", "100."],
    "SoftwareCompensationWeights": ["1.61741", "-0.00444385", "2.29683e-05", "-0.0731236", "-0.00157099", "-7.09546e-07", "0.868443", "1.0561", "-0.0238574"],
    "SplitVertexCollections": ["SplitVertices"],
    "StartVertexAlgorithmName": ["PandoraPFANew"],
    "StartVertexCollectionName": ["PandoraStartVertices"],
    "StripSplittingOn": ["0"],
    "TrackCollections": ["SelectedTracks"],
    "TrackCreatorName": ["DDTrackCreatorCLIC"],
    "TrackStateTolerance": ["0"],
    "TrackSystemName": ["DDKalTest"],
    "UnmatchedVertexTrackMaxEnergy": ["5"],
    "UseEcalScLayers": ["0"],
    "UseNonVertexTracks": ["1"],
    "UseOldTrackStateCalculation": ["0"],
    "UseUnmatchedNonVertexTracks": ["0"],
    "UseUnmatchedVertexTracks": ["1"],
    "V0VertexCollections": ["V0Vertices"],
    "YokeBarrelNormalVector": ["0", "0", "1"],
    "Z0TrackCut": ["200"],
    "Z0UnmatchedVertexTrackCut": ["5"],
    "ZCutForNonVertexTracks": ["250"]
}

#if the_args.photonEMCalibPayload:
    #DDMarlinPandora.Parameters.update(load_ddmarlin_parameter_payload(the_args.photonEMCalibPayload))
    #print(f"Loaded photon EM calibration payload: {the_args.photonEMCalibPayload}")
#if the_args.hadronicCalibPayload:
    #DDMarlinPandora.Parameters.update(load_ddmarlin_parameter_payload(the_args.hadronicCalibPayload))
    #print(f"Loaded hadronic calibration payload: {the_args.hadronicCalibPayload}")

FastJetProcessor = MarlinProcessorWrapper("FastJetProcessor")
FastJetProcessor.OutputLevel = INFO
FastJetProcessor.ProcessorType = "FastJetProcessor"
FastJetProcessor.Parameters = {
    "algorithm": ["antikt_algorithm", "0.4"],
    "clusteringMode": ["Inclusive", "5"],
    "jetOut": ["JetOut"],
    "recParticleIn": ["PandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

ValenciaJetProcessor = MarlinProcessorWrapper("ValenciaJetProcessor")
ValenciaJetProcessor.OutputLevel = INFO
ValenciaJetProcessor.ProcessorType = "FastJetProcessor"
ValenciaJetProcessor.Parameters = {
    "algorithm": ["ValenciaPlugin", "1.2", "1.0", "0.7"],
    "clusteringMode": ["ExclusiveNJets", "2"],
    "jetOut": ["ValenciaJetOut"],
    "recParticleIn": ["PandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

TrueMCintoRecoForJets = MarlinProcessorWrapper("TrueMCintoRecoForJets")
TrueMCintoRecoForJets.OutputLevel = INFO
TrueMCintoRecoForJets.ProcessorType = "TrueMCintoRecoForJets"
TrueMCintoRecoForJets.Parameters = {
    "MCParticleInputCollectionName": ["MCParticle"],
    "RECOParticleCollectionName": ["MCParticlePandoraPFOs"],
    "RecoParticleInputCollectionName": ["PandoraPFOs"],
    "RecoParticleNoLeptonCollectionName": ["PandoraPFOsNoLeptons"],
    "cosAngle_pfo_lepton": ["0.995"],
    "ignoreNeutrinosInMCJets": ["true"],
    "vetoBosonLeptons": ["false"],
    "vetoBosonLeptonsOnReco": ["false"]
}

TruthFastJetProcessor = MarlinProcessorWrapper("TruthFastJetProcessor")
TruthFastJetProcessor.OutputLevel = INFO
TruthFastJetProcessor.ProcessorType = "FastJetProcessor"
TruthFastJetProcessor.Parameters = {
    "algorithm": ["kt_algorithm", "0.4"],
    "clusteringMode": ["Inclusive", "5"],
    "jetOut": ["TruthJetOut"],
    "recParticleIn": ["MCParticlePandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

TruthValenciaJetProcessor = MarlinProcessorWrapper("TruthValenciaJetProcessor")
TruthValenciaJetProcessor.OutputLevel = INFO
TruthValenciaJetProcessor.ProcessorType = "FastJetProcessor"
TruthValenciaJetProcessor.Parameters = {
    "algorithm": ["ValenciaPlugin", "1.2", "1.0", "0.7"],
    "clusteringMode": ["ExclusiveNJets", "2"],
    "jetOut": ["TruthValenciaJetOut"],
    "recParticleIn": ["MCParticlePandoraPFOs"],
    "recombinationScheme": ["E_scheme"]
}

MyDDSimpleMuonDigi = MarlinProcessorWrapper("MyDDSimpleMuonDigi")
MyDDSimpleMuonDigi.OutputLevel = INFO
MyDDSimpleMuonDigi.ProcessorType = "DDSimpleMuonDigi"
MyDDSimpleMuonDigi.Parameters = {
    "CalibrMUON": ["70.1"],
    "MUONCollections": ["YokeBarrelCollection", "YokeEndcapCollection"],
    "MUONOutputCollection": ["MUON"],
    "MaxHitEnergyMUON": ["2.0"],
    "MuonThreshold": ["1e-06"],
    "RelationOutputCollection": ["RelationMuonHit"]
}

OverlayMIX = MarlinProcessorWrapper("OverlayMIX")
OverlayMIX.OutputLevel = INFO
OverlayMIX.ProcessorType = "OverlayTimingRandomMix"
OverlayMIX.Parameters = {
    "PathToMuPlus": [f"{the_args.data}/BIB10TeV/sim_mm_pruned/"],
    "PathToMuMinus": [f"{the_args.data}/BIB10TeV/sim_mp_pruned/"],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.18", "0.18",
        "VertexEndcapCollection", "-0.18", "0.18",
        "InnerTrackerBarrelCollection", "-0.36", "0.36",
        "InnerTrackerEndcapCollection", "-0.36", "0.36",
        "OuterTrackerBarrelCollection", "-0.36", "0.36",
        "OuterTrackerEndcapCollection", "-0.36", "0.36",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MergeMCParticles": ["false"],
    "NumberBackground": [str(the_args.overlayMixNumberBackground)]
}

OverlayIP = MarlinProcessorWrapper("OverlayIP")
OverlayIP.OutputLevel = INFO
OverlayIP.ProcessorType = "OverlayTimingGeneric"
OverlayIP.Parameters = {
    "AllowReusingBackgroundFiles": ["true"],
    "BackgroundFileNames": [
        f"{the_args.data}/IPairs/sim/sim_pairs_cycle1.slcio",
        f"{the_args.data}/IPairs/sim/sim_pairs_cycle2.slcio",
        f"{the_args.data}/IPairs/sim/sim_pairs_cycle3.slcio",
        f"{the_args.data}/IPairs/sim/sim_pairs_cycle4.slcio"
    ],
    "Collection_IntegrationTimes": [
        "VertexBarrelCollection", "-0.18", "0.18",
        "VertexEndcapCollection", "-0.18", "0.18",
        "InnerTrackerBarrelCollection", "-0.36", "0.36",
        "InnerTrackerEndcapCollection", "-0.36", "0.36",
        "OuterTrackerBarrelCollection", "-0.36", "0.36",
        "OuterTrackerEndcapCollection", "-0.36", "0.36",
        "ECalBarrelCollection", "-0.5", "15.",
        "ECalEndcapCollection", "-0.5", "15.",
        "HCalBarrelCollection", "-0.5", "15.",
        "HCalEndcapCollection", "-0.5", "15.",
        "YokeBarrelCollection", "-0.5", "15.",
        "YokeEndcapCollection", "-0.5", "15."
    ],
    "Delta_t": ["10000"],
    "IntegrationTimeMin": ["-0.5"],
    "MCParticleCollectionName": ["MCParticle"],
    "MCPhysicsParticleCollectionName": ["MCPhysicsParticles_IP"],
    "MergeMCParticles": ["false"],
    "NBunchtrain": ["1"],
    "NumberBackground": ["1"],
    "PhysicsBX": ["1"],
    "Poisson_random_NOverlay": ["false"],
    "RandomBx": ["false"],
    "StartBackgroundFileIndex": ["0"],
    "TPCDriftvelocity": ["0.05"]
}

algList.append(MyAIDAProcessor)
algList.append(EventNumber)
algList.append(InitDD4hep)
if the_args.enableBIB:
    algList.append(OverlayMIX)
if the_args.enableIP:
    algList.append(OverlayIP)
algList.append(VXDBarrelDigitiser)
algList.append(VXDEndcapDigitiser)
algList.append(InnerPlanarDigiProcessor)
algList.append(InnerEndcapPlanarDigiProcessor)
algList.append(OuterPlanarDigiProcessor)
algList.append(OuterEndcapPlanarDigiProcessor)
if not the_args.skipTrackerConing:
    algList.append(VXDBarrelConer)
    algList.append(VXDEndcapConer)
    algList.append(InnerPlanarConer)
    algList.append(InnerEndcapConer)
    algList.append(OuterPlanarConer)
    algList.append(OuterEndcapConer)
algList.append(MyEcalBarrelDigi)
algList.append(MyEcalBarrelReco)
algList.append(MyEcalEndcapDigi)
algList.append(MyEcalEndcapReco)
algList.append(MyHcalBarrelDigi)
algList.append(MyHcalBarrelReco)
algList.append(MyHcalEndcapDigi)
algList.append(MyHcalEndcapReco)
algList.append(MyEcalBarrelConer)
algList.append(MyEcalEndcapConer)
algList.append(MyHcalBarrelConer)
algList.append(MyHcalEndcapConer)
algList.append(MyEcalBarrelSelector)
algList.append(MyEcalEndcapSelector)
algList.append(MyHcalBarrelSelector)
algList.append(MyHcalEndcapSelector)
algList.append(MyDDSimpleMuonDigi)
if not the_args.skipReco:
    algList.append(CKFTracking)
    algList.append(TrackDeduper)
    algList.append(MyTrackTruth)
    algList.append(MyTrackSelectorHoles)
    algList.append(Refit)
    algList.append(MyTrackSelector)
    algList.append(MyTrackTruthSelected)
    algList.append(DDMarlinPandora)
    algList.append(FastJetProcessor)
    algList.append(ValenciaJetProcessor)
    algList.append(TrueMCintoRecoForJets)
    algList.append(TruthFastJetProcessor)
    algList.append(TruthValenciaJetProcessor)
algList.append(Output_REC)

ApplicationMgr(TopAlg=algList,
               EvtSel='NONE',
               EvtMax=-1,
               ExtSvc=[evtsvc],
               OutputLevel=INFO
               )
