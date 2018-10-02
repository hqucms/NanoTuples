import FWCore.ParameterSet.Config as cms

pfDeepBoostedJetPreprocessParams = cms.PSet(
    input_names = cms.vstring('pfcand', 
        'sv'),
    pfcand = cms.PSet(
        input_shape = cms.vuint32(1, 33, 100, 1),
        var_infos = cms.PSet(
            pfcand_VTX_ass = cms.PSet(
                median = cms.double(7.0),
                upper = cms.double(7.0)
            ),
            pfcand_btagEtaRel = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(2.38111495972)
            ),
            pfcand_btagJetDistVal = cms.PSet(
                median = cms.double(-2.72225188382e-05),
                upper = cms.double(0.0)
            ),
            pfcand_btagPParRatio = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.9845033288)
            ),
            pfcand_btagPtRatio = cms.PSet(
                median = cms.double(0.0163277750835),
                upper = cms.double(0.478605955839)
            ),
            pfcand_btagSip2dSig = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.595101356506)
            ),
            pfcand_btagSip2dVal = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.00211303704418)
            ),
            pfcand_btagSip3dSig = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(1.0722720623)
            ),
            pfcand_btagSip3dVal = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.0044621466659)
            ),
            pfcand_charge = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(1.0)
            ),
            pfcand_deltaR = cms.PSet(
                median = cms.double(0.462014108896),
                upper = cms.double(1.12555122375)
            ),
            pfcand_detadeta = cms.PSet(
                median = cms.double(3.79492393066e-09),
                upper = cms.double(1.17884007977e-06)
            ),
            pfcand_dlambdadz = cms.PSet(
                median = cms.double(-5.95361981937e-08),
                upper = cms.double(0.0)
            ),
            pfcand_dphidphi = cms.PSet(
                median = cms.double(5.3908677522e-09),
                upper = cms.double(2.9461309623e-06)
            ),
            pfcand_dphidxy = cms.PSet(
                median = cms.double(-4.71576200312e-08),
                upper = cms.double(0.0)
            ),
            pfcand_dptdpt = cms.PSet(
                median = cms.double(1.66594524842e-08),
                upper = cms.double(3.54452895408e-05)
            ),
            pfcand_drminsv = cms.PSet(
                median = cms.double(0.344621539116),
                upper = cms.double(1.23296415806)
            ),
            pfcand_dxy = cms.PSet(
                median = cms.double(-0.0),
                upper = cms.double(0.00392333976924)
            ),
            pfcand_dxydxy = cms.PSet(
                median = cms.double(4.80308813167e-07),
                upper = cms.double(4.09277672588e-05)
            ),
            pfcand_dxydz = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(9.32610788595e-08)
            ),
            pfcand_dxysig = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.561889886856)
            ),
            pfcand_dz = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.00587890623137)
            ),
            pfcand_dzdz = cms.PSet(
                median = cms.double(9.01186751889e-07),
                upper = cms.double(4.34006178693e-05)
            ),
            pfcand_dzsig = cms.PSet(
                median = cms.double(0.0),
                upper = cms.double(0.756980895996)
            ),
            pfcand_erel_log = cms.PSet(
                median = cms.double(-5.5265955925),
                upper = cms.double(-3.82370185852)
            ),
            pfcand_etarel = cms.PSet(
                median = cms.double(-0.0372355487198),
                upper = cms.double(0.363255470991)
            ),
            pfcand_lostInnerHits = cms.PSet(
                median = cms.double(-1.0),
                upper = cms.double(-1.0)
            ),
            pfcand_normchi2 = cms.PSet(
                median = cms.double(20.0),
                upper = cms.double(999.0)
            ),
            pfcand_phirel = cms.PSet(
                median = cms.double(-0.000241695306613),
                upper = cms.double(0.448083907366)
            ),
            pfcand_pt_log = cms.PSet(
                median = cms.double(0.500420093536),
                upper = cms.double(2.29867124557)
            ),
            pfcand_ptrel_log = cms.PSet(
                median = cms.double(-5.51934814453),
                upper = cms.double(-3.77376437187)
            ),
            pfcand_puppiw = cms.PSet(
                median = cms.double(1.0),
                upper = cms.double(1.0)
            ),
            pfcand_quality = cms.PSet(
                median = cms.double(5.0),
                upper = cms.double(5.0)
            )
        ),
        var_length = cms.uint32(100),
        var_names = cms.vstring('pfcand_pt_log', 
            'pfcand_ptrel_log', 
            'pfcand_erel_log', 
            'pfcand_phirel', 
            'pfcand_etarel', 
            'pfcand_deltaR', 
            'pfcand_puppiw', 
            'pfcand_drminsv', 
            'pfcand_charge', 
            'pfcand_VTX_ass', 
            'pfcand_lostInnerHits', 
            'pfcand_normchi2', 
            'pfcand_quality', 
            'pfcand_dz', 
            'pfcand_dzsig', 
            'pfcand_dxy', 
            'pfcand_dxysig', 
            'pfcand_dptdpt', 
            'pfcand_detadeta', 
            'pfcand_dphidphi', 
            'pfcand_dxydxy', 
            'pfcand_dzdz', 
            'pfcand_dxydz', 
            'pfcand_dphidxy', 
            'pfcand_dlambdadz', 
            'pfcand_btagEtaRel', 
            'pfcand_btagPtRatio', 
            'pfcand_btagPParRatio', 
            'pfcand_btagSip2dVal', 
            'pfcand_btagSip2dSig', 
            'pfcand_btagSip3dVal', 
            'pfcand_btagSip3dSig', 
            'pfcand_btagJetDistVal')
    ),
    sv = cms.PSet(
        input_shape = cms.vuint32(1, 14, 7, 1),
        var_infos = cms.PSet(
            sv_costhetasvpv = cms.PSet(
                median = cms.double(0.999728620052),
                upper = cms.double(0.999991178513)
            ),
            sv_d3d = cms.PSet(
                median = cms.double(0.443583339453),
                upper = cms.double(3.21747220039)
            ),
            sv_d3dsig = cms.PSet(
                median = cms.double(8.05331802368),
                upper = cms.double(44.3355105591)
            ),
            sv_deltaR = cms.PSet(
                median = cms.double(0.261745274067),
                upper = cms.double(0.668947582245)
            ),
            sv_dxy = cms.PSet(
                median = cms.double(0.314197361469),
                upper = cms.double(2.53855677605)
            ),
            sv_dxysig = cms.PSet(
                median = cms.double(8.03823280334),
                upper = cms.double(44.3019818115)
            ),
            sv_erel_log = cms.PSet(
                median = cms.double(-2.77814340591),
                upper = cms.double(-1.73537088871)
            ),
            sv_etarel = cms.PSet(
                median = cms.double(-0.0248847007751),
                upper = cms.double(0.202523082495)
            ),
            sv_mass = cms.PSet(
                median = cms.double(1.18997502327),
                upper = cms.double(2.93796463013)
            ),
            sv_normchi2 = cms.PSet(
                median = cms.double(0.783144414425),
                upper = cms.double(2.15780291557)
            ),
            sv_ntracks = cms.PSet(
                median = cms.double(2.0),
                upper = cms.double(4.0)
            ),
            sv_phirel = cms.PSet(
                median = cms.double(0.000566438247915),
                upper = cms.double(0.2544140172)
            ),
            sv_pt_log = cms.PSet(
                median = cms.double(3.34976601601),
                upper = cms.double(4.45681230545)
            ),
            sv_ptrel_log = cms.PSet(
                median = cms.double(-2.72588014603),
                upper = cms.double(-1.68003290653)
            )
        ),
        var_length = cms.uint32(7),
        var_names = cms.vstring('sv_pt_log', 
            'sv_ptrel_log', 
            'sv_erel_log', 
            'sv_phirel', 
            'sv_etarel', 
            'sv_deltaR', 
            'sv_mass', 
            'sv_ntracks', 
            'sv_normchi2', 
            'sv_dxy', 
            'sv_dxysig', 
            'sv_d3d', 
            'sv_d3dsig', 
            'sv_costhetasvpv')
    )
)