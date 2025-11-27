from typing import Optional
from pydantic import BaseModel, Field

class IndicadoresProgramaBase(BaseModel):
    indig_despl_viol_apr_tot: Optional[int] = None
    indig_despl_viol_cab_fam_apr_tot: Optional[int] = None
    afro_despl_viol_apr_tot: Optional[int] = None
    afro_despl_viol_cab_fam_apr_tot: Optional[int] = None
    despl_viol_apr_tot: Optional[int] = None
    despl_viol_cab_fam_apr_tot: Optional[int] = None
    despl_disc_apr_tot: Optional[int] = None
    despojo_apr_tot: Optional[int] = None
    act_grup_arm_apr_tot: Optional[int] = None
    amenaza_apr_tot: Optional[int] = None
    del_sex_apr_tot: Optional[int] = None
    desap_forz_apr_tot: Optional[int] = None
    homi_masac_apr_tot: Optional[int] = None
    minas_exp_apr_tot: Optional[int] = None
    secuestro_apr_tot: Optional[int] = None
    tortura_apr_tot: Optional[int] = None
    uso_men_grup_arm_apr_tot: Optional[int] = None
    herido_apr_tot: Optional[int] = None
    reclut_forz_apr_tot: Optional[int] = None
    negro_apr_tot: Optional[int] = None
    afro_apr_tot: Optional[int] = None
    palenq_apr_tot: Optional[int] = None
    raizal_apr_tot: Optional[int] = None
    discap_apr_tot: Optional[int] = None
    discap_aud_apr_tot: Optional[int] = None
    discap_vis_apr_tot: Optional[int] = None
    discap_fis_apr_tot: Optional[int] = None
    discap_int_apr_tot: Optional[int] = None
    discap_psico_apr_tot: Optional[int] = None
    discap_mult_apr_tot: Optional[int] = None
    sordoceg_apr_tot: Optional[int] = None
    despl_fen_nat_apr_tot: Optional[int] = None
    despl_fen_nat_cab_fam_apr_tot: Optional[int] = None
    adol_conf_ley_apr_tot: Optional[int] = None
    adol_trab_apr_tot: Optional[int] = None
    indig_apr_tot: Optional[int] = None
    inpec_apr_tot: Optional[int] = None
    jov_vuln_apr_tot: Optional[int] = None
    muj_cabfam_apr_tot: Optional[int] = None
    proc_reint_apr_tot: Optional[int] = None
    ado_desv_gr_arm_tot: Optional[int] = None
    rem_pal_tot: Optional[int] = None
    sob_min_ant_tot: Optional[int] = None
    sold_camp_tot: Optional[int] = None
    terc_edad_tot: Optional[int] = None
    rom_tot: Optional[int] = None
    camp_tot: Optional[int] = None
    ning_tot: Optional[int] = None
    artes_tot: Optional[int] = None
    empr_tot: Optional[int] = None
    mic_emp_tot: Optional[int] = None
    rem_cie_tot: Optional[int] = None
    gran_total: Optional[int] = None


class CrearIndicadoresPrograma(IndicadoresProgramaBase):
    cod_programa: int


class RetornoIndicadoresPrograma(IndicadoresProgramaBase):
    cod_programa: int


class EditarIndicadoresPrograma(BaseModel):
    cod_programa: Optional[int] = None
    indig_despl_viol_apr_tot: Optional[int] = None
    indig_despl_viol_cab_fam_apr_tot: Optional[int] = None
    afro_despl_viol_apr_tot: Optional[int] = None
    afro_despl_viol_cab_fam_apr_tot: Optional[int] = None
    despl_viol_apr_tot: Optional[int] = None
    despl_viol_cab_fam_apr_tot: Optional[int] = None
    despl_disc_apr_tot: Optional[int] = None
    despojo_apr_tot: Optional[int] = None
    act_grup_arm_apr_tot: Optional[int] = None
    amenaza_apr_tot: Optional[int] = None
    del_sex_apr_tot: Optional[int] = None
    desap_forz_apr_tot: Optional[int] = None
    homi_masac_apr_tot: Optional[int] = None
    minas_exp_apr_tot: Optional[int] = None
    secuestro_apr_tot: Optional[int] = None
    tortura_apr_tot: Optional[int] = None
    uso_men_grup_arm_apr_tot: Optional[int] = None
    herido_apr_tot: Optional[int] = None
    reclut_forz_apr_tot: Optional[int] = None
    negro_apr_tot: Optional[int] = None
    afro_apr_tot: Optional[int] = None
    palenq_apr_tot: Optional[int] = None
    raizal_apr_tot: Optional[int] = None
    discap_apr_tot: Optional[int] = None
    discap_aud_apr_tot: Optional[int] = None
    discap_vis_apr_tot: Optional[int] = None
    discap_fis_apr_tot: Optional[int] = None
    discap_int_apr_tot: Optional[int] = None
    discap_psico_apr_tot: Optional[int] = None
    discap_mult_apr_tot: Optional[int] = None
    sordoceg_apr_tot: Optional[int] = None
    despl_fen_nat_apr_tot: Optional[int] = None
    despl_fen_nat_cab_fam_apr_tot: Optional[int] = None
    adol_conf_ley_apr_tot: Optional[int] = None
    adol_trab_apr_tot: Optional[int] = None
    indig_apr_tot: Optional[int] = None
    inpec_apr_tot: Optional[int] = None
    jov_vuln_apr_tot: Optional[int] = None
    muj_cabfam_apr_tot: Optional[int] = None
    proc_reint_apr_tot: Optional[int] = None
    ado_desv_gr_arm_tot: Optional[int] = None
    rem_pal_tot: Optional[int] = None
    sob_min_ant_tot: Optional[int] = None
    sold_camp_tot: Optional[int] = None
    terc_edad_tot: Optional[int] = None
    rom_tot: Optional[int] = None
    camp_tot: Optional[int] = None
    ning_tot: Optional[int] = None
    artes_tot: Optional[int] = None
    empr_tot: Optional[int] = None
    mic_emp_tot: Optional[int] = None
    rem_cie_tot: Optional[int] = None
    gran_total: Optional[int] = None
