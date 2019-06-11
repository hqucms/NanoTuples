import FWCore.ParameterSet.Config as cms

pfMassDecorrelatedDeepBoostedJetPreprocessParams = cms.PSet(
    input_names = cms.vstring(
        'pf_points', 
        'pf_features', 
        'pf_mask', 
        'sv_points', 
        'sv_features', 
        'sv_mask'
    ),
    pf_features = cms.PSet(
        input_shape = cms.vuint32(1, 36, 100),
        var_infos = cms.PSet(
            pfcand_VTX_ass = cms.PSet(
                median = cms.double(7.0),
                norm_factor = cms.double(0.5)
            ),
            pfcand_abseta = cms.PSet(
                median = cms.double(0.684469103813),
                norm_factor = cms.double(1.42850297166)
            ),
            pfcand_btagEtaRel = cms.PSet(
                median = cms.double(0.255159556866),
                norm_factor = cms.double(0.468699885943)
            ),
            pfcand_btagJetDistVal = cms.PSet(
                median = cms.double(-8.81981977727e-05),
                norm_factor = cms.double(140.522178125)
            ),
            pfcand_btagPParRatio = cms.PSet(
                median = cms.double(0.252265334129),
                norm_factor = cms.double(1.36492167971)
            ),
            pfcand_btagPtRatio = cms.PSet(
                median = cms.double(0.0196897052228),
                norm_factor = cms.double(1.9784610168)
            ),
            pfcand_btagSip2dSig = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.67308389176)
            ),
            pfcand_btagSip2dVal = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(459.70770887)
            ),
            pfcand_btagSip3dSig = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(0.928893542833)
            ),
            pfcand_btagSip3dVal = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(218.172542714)
            ),
            pfcand_charge = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.0)
            ),
            pfcand_deltaR = cms.PSet(
                median = cms.double(0.495622307062),
                norm_factor = cms.double(1.500319139)
            ),
            pfcand_detadeta = cms.PSet(
                median = cms.double(7.68575070254e-09),
                norm_factor = cms.double(747738.167462)
            ),
            pfcand_dlambdadz = cms.PSet(
                median = cms.double(-9.515525079e-08),
                norm_factor = cms.double(131502.743809)
            ),
            pfcand_dphidphi = cms.PSet(
                median = cms.double(8.37077873683e-09),
                norm_factor = cms.double(299793.094059)
            ),
            pfcand_dphidxy = cms.PSet(
                median = cms.double(-7.175672323e-08),
                norm_factor = cms.double(85859.9801358)
            ),
            pfcand_dptdpt = cms.PSet(
                median = cms.double(2.86818817585e-08),
                norm_factor = cms.double(23859.2166445)
            ),
            pfcand_drminsvin = cms.PSet(
                median = cms.double(0.399680674076),
                norm_factor = cms.double(1.07536943435)
            ),
            pfcand_drsubjet1 = cms.PSet(
                median = cms.double(0.513681173325),
                norm_factor = cms.double(1.39343340574)
            ),
            pfcand_drsubjet2 = cms.PSet(
                median = cms.double(0.629831254482),
                norm_factor = cms.double(1.44021205362)
            ),
            pfcand_dxy = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(241.367128211)
            ),
            pfcand_dxydxy = cms.PSet(
                median = cms.double(7.11589109414e-07),
                norm_factor = cms.double(22717.2485631)
            ),
            pfcand_dxydz = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(10067441.7293)
            ),
            pfcand_dxysig = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.7570628556)
            ),
            pfcand_dz = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(161.76935424)
            ),
            pfcand_dzdz = cms.PSet(
                median = cms.double(1.2530085769e-06),
                norm_factor = cms.double(21887.5856883)
            ),
            pfcand_dzsig = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.31464525548)
            ),
            pfcand_erel_log = cms.PSet(
                median = cms.double(-5.59631967545),
                norm_factor = cms.double(0.588267796738)
            ),
            pfcand_etarel = cms.PSet(
                median = cms.double(-0.0356653742492),
                norm_factor = cms.double(2.05963443228)
            ),
            pfcand_lostInnerHits = cms.PSet(
                median = cms.double(-1.0),
                norm_factor = cms.double(1.0)
            ),
            pfcand_normchi2 = cms.PSet(
                median = cms.double(4.0),
                norm_factor = cms.double(0.00100502512563)
            ),
            pfcand_phirel = cms.PSet(
                median = cms.double(-0.000222183996812),
                norm_factor = cms.double(2.10409983468)
            ),
            pfcand_pt_log = cms.PSet(
                median = cms.double(0.448783993721),
                norm_factor = cms.double(0.556309265638)
            ),
            pfcand_ptrel_log = cms.PSet(
                median = cms.double(-5.58238124847),
                norm_factor = cms.double(0.575621493033)
            ),
            pfcand_puppiw = cms.PSet(
                median = cms.double(1.0),
                norm_factor = cms.double(255.000015199)
            ),
            pfcand_quality = cms.PSet(
                median = cms.double(5.0),
                norm_factor = cms.double(0.2)
            )
        ),
        var_length = cms.uint32(100),
        var_names = cms.vstring(
            'pfcand_pt_log', 
            'pfcand_ptrel_log', 
            'pfcand_erel_log', 
            'pfcand_phirel', 
            'pfcand_etarel', 
            'pfcand_deltaR', 
            'pfcand_abseta', 
            'pfcand_puppiw', 
            'pfcand_drminsvin', 
            'pfcand_drsubjet1', 
            'pfcand_drsubjet2', 
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
            'pfcand_btagJetDistVal'
        )
    ),
    pf_mask = cms.PSet(
        input_shape = cms.vuint32(1, 1, 100),
        var_infos = cms.PSet(
            pfcand_mask = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.0)
            )
        ),
        var_length = cms.uint32(100),
        var_names = cms.vstring('pfcand_mask')
    ),
    pf_points = cms.PSet(
        input_shape = cms.vuint32(1, 2, 100),
        var_infos = cms.PSet(
            pfcand_etarel = cms.PSet(
                median = cms.double(-0.0356653742492),
                norm_factor = cms.double(2.05963443228)
            ),
            pfcand_phirel = cms.PSet(
                median = cms.double(-0.000222183996812),
                norm_factor = cms.double(2.10409983468)
            )
        ),
        var_length = cms.uint32(100),
        var_names = cms.vstring(
            'pfcand_etarel', 
            'pfcand_phirel'
        )
    ),
    sv_features = cms.PSet(
        input_shape = cms.vuint32(1, 15, 7),
        var_infos = cms.PSet(
            sv_abseta = cms.PSet(
                median = cms.double(0.658988654613),
                norm_factor = cms.double(1.40940489685)
            ),
            sv_costhetasvpv = cms.PSet(
                median = cms.double(0.999707758427),
                norm_factor = cms.double(176.703682998)
            ),
            sv_d3d = cms.PSet(
                median = cms.double(0.409971952438),
                norm_factor = cms.double(0.355778059196)
            ),
            sv_d3dsig = cms.PSet(
                median = cms.double(7.35935544968),
                norm_factor = cms.double(0.0285860300182)
            ),
            sv_deltaR = cms.PSet(
                median = cms.double(0.256634920835),
                norm_factor = cms.double(2.12633100784)
            ),
            sv_dxy = cms.PSet(
                median = cms.double(0.287629932165),
                norm_factor = cms.double(0.441527021352)
            ),
            sv_dxysig = cms.PSet(
                median = cms.double(7.34407329559),
                norm_factor = cms.double(0.0286021748557)
            ),
            sv_erel_log = cms.PSet(
                median = cms.double(-2.82480883598),
                norm_factor = cms.double(0.710537129373)
            ),
            sv_etarel = cms.PSet(
                median = cms.double(-0.0208502989262),
                norm_factor = cms.double(3.77103200621)
            ),
            sv_mass = cms.PSet(
                median = cms.double(1.17351639271),
                norm_factor = cms.double(0.556046977606)
            ),
            sv_normchi2 = cms.PSet(
                median = cms.double(0.768759608269),
                norm_factor = cms.double(0.731017386896)
            ),
            sv_ntracks = cms.PSet(
                median = cms.double(2.0),
                norm_factor = cms.double(0.5)
            ),
            sv_phirel = cms.PSet(
                median = cms.double(0.000620208273176),
                norm_factor = cms.double(3.83182744354)
            ),
            sv_pt_log = cms.PSet(
                median = cms.double(3.30453014374),
                norm_factor = cms.double(0.703660600579)
            ),
            sv_ptrel_log = cms.PSet(
                median = cms.double(-2.77152013779),
                norm_factor = cms.double(0.693486069718)
            )
        ),
        var_length = cms.uint32(7),
        var_names = cms.vstring(
            'sv_pt_log', 
            'sv_ptrel_log', 
            'sv_erel_log', 
            'sv_phirel', 
            'sv_etarel', 
            'sv_deltaR', 
            'sv_abseta', 
            'sv_mass', 
            'sv_ntracks', 
            'sv_normchi2', 
            'sv_dxy', 
            'sv_dxysig', 
            'sv_d3d', 
            'sv_d3dsig', 
            'sv_costhetasvpv'
        )
    ),
    sv_mask = cms.PSet(
        input_shape = cms.vuint32(1, 1, 7),
        var_infos = cms.PSet(
            sv_mask = cms.PSet(
                median = cms.double(0.0),
                norm_factor = cms.double(1.0)
            )
        ),
        var_length = cms.uint32(7),
        var_names = cms.vstring('sv_mask')
    ),
    sv_points = cms.PSet(
        input_shape = cms.vuint32(1, 2, 7),
        var_infos = cms.PSet(
            sv_etarel = cms.PSet(
                median = cms.double(-0.0208502989262),
                norm_factor = cms.double(3.77103200621)
            ),
            sv_phirel = cms.PSet(
                median = cms.double(0.000620208273176),
                norm_factor = cms.double(3.83182744354)
            )
        ),
        var_length = cms.uint32(7),
        var_names = cms.vstring(
            'sv_etarel', 
            'sv_phirel'
        )
    )
)
