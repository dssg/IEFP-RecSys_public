DROP DATABASE IF EXISTS iefp;

CREATE DATABASE iefp;

--table ofertas
DROP TABLE IF EXISTS ofertas;

CREATE TABLE ofertas (
	ano_mes VARCHAR ,
	tipo_movimento DECIMAL ,
	centro VARCHAR ,
	cnp VARCHAR ,
	ind_cnp DECIMAL ,
	a_tempo VARCHAR ,
	natureza_emprego VARCHAR ,
	nr_meses DECIMAL,
	idade_minima VARCHAR,
	idade_maxima VARCHAR,
	habilitacoes_minima VARCHAR,
	habilitacoes_maximo VARCHAR,
	salario DECIMAL,
	tipo_salario VARCHAR,
	transporte_proprio VARCHAR,
	carta_conducao VARCHAR,
	formacao_profissional VARCHAR,
	frances VARCHAR,
	ingles VARCHAR,
	alemao VARCHAR,
	espanhol VARCHAR,
	outra_lingua VARCHAR,
	area_recrutamento VARCHAR,
	freguesia_local_trabalho VARCHAR,
	data_comunicacao TIMESTAMP WITHOUT TIME ZONE,
	modo_comunicacao VARCHAR ,
	nr_postos_trabalho DECIMAL ,
	data_validade TIMESTAMP WITHOUT TIME ZONE,
	freguesia_residencia_1 VARCHAR,
	freguesia_residencia_2 VARCHAR,
	freguesia_residencia_3 VARCHAR,
	data_anulacao TIMESTAMP WITHOUT TIME ZONE,
	motivo_anulacao VARCHAR,
	nr_oferta VARCHAR ,
	data_movimento TIMESTAMP WITHOUT TIME ZONE,
	freguesia_entidade VARCHAR,
	cae_entidade_v2 VARCHAR,
	ind1_cae_v2 VARCHAR,
	ind2_cae_v2 VARCHAR,
	nr_pessoas_servico DECIMAL ,
	centro_movimento VARCHAR ,
	data_insercao TIMESTAMP WITHOUT TIME ZONE,
	saldo_pt DECIMAL ,
	cnp_pretendida VARCHAR,
	qualificacoes VARCHAR,
	tempo_pratica_min VARCHAR,
	tempo_pratica_max VARCHAR,
	area_curso VARCHAR,
	qualificacoes_candidato DECIMAL,
	data_ultima_divulgacao TIMESTAMP WITHOUT TIME ZONE,
	nivel_divulgacao DECIMAL ,
	origem_oferta VARCHAR ,
	pais_eures VARCHAR,
	centro_ute VARCHAR,
	nipc VARCHAR ,
	cod_subentidade VARCHAR ,
	cnatureza_juridica VARCHAR ,
	tempo_permanencia VARCHAR,
	recrutamento_internacional VARCHAR,
	data_rec_internacional TIMESTAMP WITHOUT TIME ZONE,
	data_limite_divulgacao TIMESTAMP WITHOUT TIME ZONE,
	tipo_actividade VARCHAR,
	sub_transporte VARCHAR,
	sub_turno VARCHAR,
	sub_refeicao VARCHAR,
	utilizador VARCHAR,
	contingente VARCHAR,
	cae_entidade DECIMAL ,
	ind1_cae VARCHAR ,
	ind2_cae VARCHAR ,
	acompanhada VARCHAR,
	goe VARCHAR,
	me2012 VARCHAR,
	id_estabel VARCHAR,
	regime_horario VARCHAR,
	protocolo VARCHAR,
	cod_protocolo VARCHAR,
	autoriza_consulta_acordo_sect VARCHAR,
	reducao_tsu VARCHAR,
	nivel_intermediacao VARCHAR,
	data_afetacao_tecnico VARCHAR,
	origem_registo_ofa VARCHAR,
	motivo_invalidacao VARCHAR,
	id_reg_ent VARCHAR,
	centroa VARCHAR,
	startup VARCHAR,
	tsu45 VARCHAR,
	me2013 VARCHAR,
	reembolso_tsu VARCHAR,
	processo_recup_empresas VARCHAR,
	cpp VARCHAR,
	ind_cpp VARCHAR,
	cpp_pretendida VARCHAR,
	me2014 VARCHAR,
	eao VARCHAR,
	e_mais VARCHAR,
	pais_residencia_estrang VARCHAR,
	grau_habilitacao_estrang VARCHAR,
	last_update_date VARCHAR
);

\copy ofertas from '/data/EMP_OFERTAS.csv' with csv header; --

--we copy first so that it wont take too much time, then we create the index.
CREATE INDEX ofertas_idx_nr_oferta on ofertas(nr_oferta);



--table pedidos
drop table if exists pedidos;

CREATE TABLE pedidos (
	ano_mes DECIMAL ,
	tipo_movimento DECIMAL ,
	centro DECIMAL ,
	nr_utente DECIMAL ,
	cnp_pretendida DECIMAL ,
	ind_cnp DECIMAL ,
	cae_anterior_v2 VARCHAR,
	ind1_cae_v2 VARCHAR,
	ind2_cae_v2 VARCHAR,
	data_movimento TIMESTAMP WITHOUT TIME ZONE,
	freguesia VARCHAR ,
	nacionalidade VARCHAR ,
	idade DECIMAL ,
	sexo VARCHAR ,
	habilitacao VARCHAR ,
	pais_emigracao VARCHAR,
	deficiencia DECIMAL ,
	categoria DECIMAL ,
	motivo_inscricao DECIMAL ,
	rinsc VARCHAR ,
	estado_civil VARCHAR ,
	nr_pessoas_cargo DECIMAL,
	tempo_inscricao DECIMAL ,
	tempo_pratica DECIMAL,
	local_trabalho VARCHAR,
	a_tempo VARCHAR ,
	natureza_emprego VARCHAR ,
	ucnp DECIMAL,
	tempo_pratica_ucnp DECIMAL,
	subsidio VARCHAR,
	cnp_colocacao DECIMAL,
	cae_colocacao_v2 VARCHAR,
	local_colocacao VARCHAR,
	natureza_colocacao VARCHAR,
	data_colocacao TIMESTAMP WITHOUT TIME ZONE,
	data_anulacao TIMESTAMP WITHOUT TIME ZONE,
	motivo_anulacao DECIMAL,
	plano_emprego VARCHAR ,
	ute_id DECIMAL ,
	rmg VARCHAR ,
	centro_movimento DECIMAL ,
	data_inscricao TIMESTAMP WITHOUT TIME ZONE,
	data_nascimento TIMESTAMP WITHOUT TIME ZONE,
	motivo_anterior_saida DECIMAL,
	pais_colocacao VARCHAR,
	regime_trabalho_colocacao VARCHAR,
	qualificacao DECIMAL,
	rmg_anterior VARCHAR ,
	motivo_fim_rmg DECIMAL,
	ppe_anterior VARCHAR ,
	tipo_doc_id VARCHAR ,
	formacao_profissional VARCHAR,
	areas_curso VARCHAR,
	data_prim_candidatura TIMESTAMP WITHOUT TIME ZONE,
	data_n_reinsc TIMESTAMP WITHOUT TIME ZONE,
	motivo_visita DECIMAL ,
	centro_np DECIMAL,
	cod_prog_sief VARCHAR,
	estado VARCHAR ,
	data_ultima_saida TIMESTAMP WITHOUT TIME ZONE,
	origem_candidatura VARCHAR,
	carteira_profissional VARCHAR,
	rsi VARCHAR,
	motivo_indisponibilidade DECIMAL,
	data_fim_indisponivel TIMESTAMP WITHOUT TIME ZONE,
	sd_motivo_desemprego VARCHAR,
	apresentacao_quinzenal VARCHAR ,
	pae VARCHAR ,
	declaracao_ent_empregadora VARCHAR,
	advert_notif VARCHAR,
	tipo_notificacao_ocorrencia VARCHAR,
	tipo_resultado_notificacao VARCHAR,
	cest_superior DECIMAL,
	ano_conclusao_curso DECIMAL,
	recrutamento_internacional VARCHAR,
	data_rec_internacional VARCHAR,
	tipo_actividade VARCHAR,
	utilizador VARCHAR,
	cae_anterior DECIMAL,
	ind1_cae DECIMAL,
	ind2_cae DECIMAL,
	cae_colocacao DECIMAL,
	id_conjuge VARCHAR,
	estado_civ_conjuge VARCHAR,
	categoria_conjuge VARCHAR,
	estado_conjuge VARCHAR,
	motiv_indisp_conjuge VARCHAR,
	tipo_ocupacao VARCHAR,
	data_desemprego VARCHAR,
	categoria_anterior VARCHAR,
	estado_anterior VARCHAR,
	cod_intervencao VARCHAR,
	ccrss VARCHAR,
	motivo_indisponibilidade_ant VARCHAR,
	me2012 VARCHAR,
	id_estabel VARCHAR,
	id_oferta VARCHAR,
	data_subsidio VARCHAR,
	descendentes_a_cargo VARCHAR,
	subsidio_conjuge VARCHAR,
	regime_horario VARCHAR,
	sub_decreto_lei VARCHAR,
	sub_data_indef VARCHAR,
	sub_data_inicio VARCHAR,
	sub_data_fim VARCHAR,
	sub_tempo_previsto VARCHAR,
	sub_valor VARCHAR,
	sub_data_extincao VARCHAR,
	sub_data_suspensao VARCHAR,
	sub_data_reinicio VARCHAR,
	sub_cod_motivo_cessacao VARCHAR,
	sub_cod_motivo_suspensao VARCHAR,
	gestor_carreira VARCHAR,
	segmento VARCHAR,
	data_afetacao_tecnico VARCHAR,
	origem_registo_utente VARCHAR,
	motivo_invalidacao VARCHAR,
	data_elaboracao_ppe VARCHAR,
	centroa VARCHAR,
	num_pedidos_esclar VARCHAR,
	data_pedido_ult_ped_esclar VARCHAR,
	data_resposta_ult_ped_esclar VARCHAR,
	me2013 VARCHAR,
	reembolso_tsu VARCHAR,
	tempo_pratica_ucpp VARCHAR,
	ucpp VARCHAR,
	cpp_pretendida VARCHAR,
	ind_cpp VARCHAR,
	cpp_colocacao VARCHAR,
	enicc VARCHAR,
	gj VARCHAR,
	data_inicio_gj VARCHAR,
	data_primeira_resposta_gj VARCHAR,
	gj_anterior VARCHAR,
	motivo_nao_sinalizacao_gj VARCHAR,
	motivo_fim_gj VARCHAR,
	data_fim VARCHAR,
	me2014 VARCHAR,
	primeira_resposta_tie_cod_gj VARCHAR,
	data_ultimo_contacto VARCHAR,
	tuc_codigo VARCHAR,
	eao VARCHAR,
	e_mais VARCHAR,
	feg VARCHAR,
	tipo_feg VARCHAR,
	rp VARCHAR,
	nce_cnacionalidade_rp VARCHAR,
	pais_residencia_estrang VARCHAR,
	grau_habilitacao_estrang VARCHAR,
	last_update_date VARCHAR
);

\copy pedidos from '/data/emp_pedidos.csv' with csv header; --37,317,447

CREATE INDEX pedidos_idx_ute_id on pedidos(ute_id);
CREATE INDEX pedidos_idx_data_movimento on pedidos(data_movimento);
CREATE INDEX pedidos_idx_ute_id_data_movimento on pedidos(ute_id, data_movimento);
CREATE INDEX pedidos_idx_ano_mes on pedidos(ano_mes);
CREATE INDEX pedidos_idx_tipo_movimento on pedidos(tipo_movimento);
CREATE INDEX pedidos_idx_sexo on pedidos(sexo);
CREATE INDEX pedidos_idx_centro on pedidos(centro);


--table apresentados
DROP TABLE IF EXISTS apresentados;

CREATE TABLE apresentados (
	ano_mes DECIMAL ,
	tipo_movimento DECIMAL ,
	centro DECIMAL ,
	nr_utente DECIMAL ,
	tipo VARCHAR,
	data_apresentacao TIMESTAMP WITHOUT TIME ZONE,
	nr_oferta DECIMAL ,
	cnp_oferta DECIMAL,
	resultado_apresentacao DECIMAL,
	data_resultado TIMESTAMP WITHOUT TIME ZONE,
	data_movimento TIMESTAMP WITHOUT TIME ZONE,
	freguesia VARCHAR ,
	idade DECIMAL ,
	sexo VARCHAR ,
	habilitacao VARCHAR,
	ppe VARCHAR ,
	categoria DECIMAL ,
	cnp_pretendida DECIMAL ,
	tempo_inscricao DECIMAL ,
	tipo_utente VARCHAR ,
	ute_id DECIMAL ,
	rmg VARCHAR ,
	centro_movimento DECIMAL ,
	data_nascimento TIMESTAMP WITHOUT TIME ZONE,
	data_inscricao TIMESTAMP WITHOUT TIME ZONE,
	nacionalidade VARCHAR,
	deficiencia DECIMAL ,
	rmg_anterior VARCHAR ,
	motivo_fim_rmg DECIMAL,
	estado_civil VARCHAR ,
	nr_pessoas_cargo DECIMAL,
	cae_anterior_v2 VARCHAR,
	cae_entidade_v2 VARCHAR,
	origem_oferta VARCHAR ,
	pais_eures VARCHAR,
	carteira_profissional VARCHAR,
	qualificacao DECIMAL,
	ppe_anterior VARCHAR ,
	cnp_anterior DECIMAL,
	subsidio DECIMAL,
	local_trabalho VARCHAR ,
	tipo_candidatura_externa VARCHAR,
	tipo_contrato_pretendido VARCHAR ,
	regime_trabalho_pretendido VARCHAR ,
	formacao_profissional VARCHAR,
	areas_curso VARCHAR,
	tipo_doc_id VARCHAR,
	tempo_pratica_ucnp DECIMAL,
	tempo_pratica DECIMAL,
	centro_np DECIMAL,
	estado VARCHAR,
	apresentacao_directa VARCHAR,
	centro_ofa DECIMAL ,
	rsi VARCHAR,
	sd_motivo_desemprego VARCHAR,
	apresentacao_quinzenal VARCHAR ,
	pae VARCHAR ,
	cest_superior DECIMAL,
	ano_conclusao_curso DECIMAL,
	utilizador VARCHAR,
	cae_anterior DECIMAL,
	cae_entidade DECIMAL,
	acompanhada VARCHAR,
	cae_prioritaria VARCHAR,
	tipo_ocupacao VARCHAR,
	data_desemprego VARCHAR,
	me2012 VARCHAR,
	id_apresentacao VARCHAR,
	id_estabel VARCHAR,
	data_subsidio VARCHAR,
	descendentes_a_cargo VARCHAR,
	subsidio_conjuge VARCHAR,
	id_conjuge VARCHAR,
	categoria_conjuge VARCHAR,
	estado_conjuge VARCHAR,
	motiv_indisp_conjuge VARCHAR,
	reducao_tsu VARCHAR,
	gestor_carreira VARCHAR,
	segmento VARCHAR,
	origem_registo_utente VARCHAR,
	origem_registo_ofa VARCHAR,
	data_afetacao_tecnico VARCHAR,
	data_afetacao_tecnico_ofa VARCHAR,
	nivel_intermediacao VARCHAR,
	data_elaboracao_ppe VARCHAR,
	centroa VARCHAR,
	me2013 VARCHAR,
	reembolso_tsu VARCHAR,
	processo_recup_empresas VARCHAR,
	cpp_pretendida VARCHAR,
	cpp_oferta VARCHAR,
	cpp_anterior VARCHAR,
	startup VARCHAR,
	tsu45 VARCHAR,
	tempo_pratica_ucpp VARCHAR,
	enicc VARCHAR,
	gj VARCHAR,
	data_inicio_gj VARCHAR,
	data_primeira_resposta_gj VARCHAR,
	me2014 VARCHAR,
	motivo_nao_sinalizacao_gj VARCHAR,
	eao VARCHAR,
	e_mais VARCHAR,
	feg VARCHAR,
	tipo_feg VARCHAR,
	rp VARCHAR,
	nce_cnacionalidade_rp VARCHAR,
	pais_residencia_estrang VARCHAR,
	grau_habilitacao_estrang VARCHAR,
	last_update_date VARCHAR
);

\COPY apresentados from '/data/MOV_APRESENTADOS.csv' with csv header; --13,989,614

CREATE INDEX apresentados_idx_ute_id on apresentados(ute_id);
CREATE INDEX apresentados_idx_nr_oferta on apresentados(nr_oferta);
CREATE INDEX apresentados_idx_data_movimento on apresentados(data_movimento);



--table convocados
DROP TABLE IF EXISTS convocados;

CREATE TABLE convocados (
	ano_mes DECIMAL ,
	tipo_movimento DECIMAL ,
	centro DECIMAL ,
	nr_utente DECIMAL ,
	tipo VARCHAR ,
	convocado_para TIMESTAMP WITHOUT TIME ZONE,
	nr_oferta DECIMAL,
	convocado_em TIMESTAMP WITHOUT TIME ZONE,
	resultado DECIMAL,
	data_resultado TIMESTAMP WITHOUT TIME ZONE,
	data_movimento TIMESTAMP WITHOUT TIME ZONE,
	freguesia VARCHAR ,
	idade DECIMAL ,
	sexo VARCHAR ,
	habilitacao VARCHAR ,
	ppe VARCHAR ,
	categoria DECIMAL,
	cnp_pretendida DECIMAL,
	tempo_inscricao DECIMAL,
	tipo_utente VARCHAR ,
	ute_id DECIMAL ,
	rmg VARCHAR ,
	centro_movimento DECIMAL ,
	data_nascimento TIMESTAMP WITHOUT TIME ZONE,
	data_inscricao TIMESTAMP WITHOUT TIME ZONE,
	nacionalidade VARCHAR ,
	deficiencia DECIMAL ,
	rmg_anterior VARCHAR ,
	motivo_fim_rmg DECIMAL,
	estado_civil VARCHAR ,
	nr_pessoas_cargo DECIMAL,
	cae_anterior_v2 VARCHAR,
	carteira_profissional VARCHAR,
	qualificacao DECIMAL,
	ppe_anterior VARCHAR ,
	cnp_anterior DECIMAL,
	subsidio DECIMAL,
	origem_oferta VARCHAR,
	pais_eures VARCHAR,
	local_trabalho VARCHAR,
	tipo_candidatura_externa VARCHAR,
	tipo_contrato_pretendido VARCHAR,
	regime_trabalho_pretendido VARCHAR,
	formacao_profissional VARCHAR,
	areas_curso VARCHAR,
	tipo_doc_id VARCHAR ,
	tempo_pratica_ucnp DECIMAL,
	tempo_pratica DECIMAL,
	centro_np DECIMAL,
	estado VARCHAR,
	centro_ofa DECIMAL,
	rsi VARCHAR,
	sd_motivo_desemprego VARCHAR,
	apresentacao_quinzenal VARCHAR ,
	pae VARCHAR ,
	cest_superior DECIMAL,
	ano_conclusao_curso DECIMAL,
	utilizador VARCHAR ,
	cae_anterior DECIMAL,
	cod_req_rsi VARCHAR,
	tipo_ocupacao VARCHAR,
	data_desemprego VARCHAR,
	id_convocatoria VARCHAR,
	data_subsidio VARCHAR,
	descendentes_a_cargo VARCHAR,
	subsidio_conjuge VARCHAR,
	id_conjuge VARCHAR,
	categoria_conjuge VARCHAR,
	estado_conjuge VARCHAR,
	motiv_indisp_conjuge VARCHAR,
	gestor_carreira VARCHAR,
	segmento VARCHAR,
	origem_registo_utente VARCHAR,
	data_afetacao_tecnico VARCHAR,
	data_elaboracao_ppe VARCHAR,
	centroa VARCHAR,
	idconvocatoria_ant VARCHAR,
	cpp_pretendida VARCHAR,
	tempo_pratica_ucpp VARCHAR,
	cpp_anterior VARCHAR,
	gj VARCHAR,
	data_inicio_gj VARCHAR,
	data_primeira_resposta_gj VARCHAR,
	motivo_nao_sinalizacao_gj VARCHAR,
	tipo_sessao VARCHAR,
	feg VARCHAR,
	tipo_feg VARCHAR,
	rp VARCHAR,
	nce_cnacionalidade_rp VARCHAR,
	pais_residencia_estrang VARCHAR,
	grau_habilitacao_estrang VARCHAR,
	last_update_date VARCHAR
);

\COPY  convocados from '/data/MOV_CONVOCADOS.csv' with csv header; --38,498,895


CREATE INDEX convocados_idx_ute_id on convocados(ute_id);
CREATE INDEX convocados_idx_nr_oferta on convocados(nr_oferta);
CREATE INDEX convocados_idx_data_movimento on convocados(data_movimento);


--table intervencoes
DROP TABLE IF EXISTS intervencoes;

CREATE TABLE intervencoes (
	ano_mes DECIMAL ,
	tipo_movimento DECIMAL ,
	centro DECIMAL ,
	nr_utente DECIMAL ,
	codigo_intervencao DECIMAL ,
	data_intervencao TIMESTAMP WITHOUT TIME ZONE,
	sessao DECIMAL,
	area_intervencao DECIMAL,
	data_resultado TIMESTAMP WITHOUT TIME ZONE,
	resultado_intervencao DECIMAL,
	data_movimento TIMESTAMP WITHOUT TIME ZONE,
	freguesia VARCHAR ,
	idade VARCHAR ,
	sexo VARCHAR ,
	habilitacao VARCHAR ,
	ppe VARCHAR ,
	categoria DECIMAL,
	cnp_pretendida DECIMAL,
	tempo_inscricao DECIMAL,
	tipo_utente VARCHAR ,
	ute_id DECIMAL ,
	rmg VARCHAR ,
	centro_movimento VARCHAR ,
	data_nascimento TIMESTAMP WITHOUT TIME ZONE,
	data_inscricao TIMESTAMP WITHOUT TIME ZONE,
	nacionalidade VARCHAR ,
	deficiencia DECIMAL ,
	rmg_anterior VARCHAR ,
	motivo_fim_rmg DECIMAL,
	estado_civil VARCHAR ,
	nr_pessoas_cargo DECIMAL,
	cae_anterior_v2 VARCHAR,
	carteira_profissional VARCHAR,
	qualificacao DECIMAL,
	ppe_anterior VARCHAR ,
	cnp_anterior DECIMAL,
	subsidio VARCHAR,
	local_trabalho VARCHAR,
	tipo_candidatura_externa VARCHAR,
	tipo_contrato_pretendido VARCHAR,
	regime_trabalho_pretendido VARCHAR,
	formacao_profissional VARCHAR,
	areas_curso VARCHAR,
	tipo_doc_id VARCHAR ,
	tempo_pratica_ucnp DECIMAL,
	tempo_pratica VARCHAR,
	centro_np VARCHAR,
	estado VARCHAR,
	rsi VARCHAR,
	ambito VARCHAR,
	pri VARCHAR,
	projecto VARCHAR,
	ito_eco VARCHAR ,
	tipo VARCHAR,
	tipo_encaminhamento VARCHAR ,
	ccentro_ins DECIMAL,
	ccentro DECIMAL,
	afirmativo VARCHAR,
	f_dcurso VARCHAR,
	f_horas DECIMAL,
	f_cmod_form DECIMAL,
	f_data_inicio TIMESTAMP WITHOUT TIME ZONE,
	f_data_fim TIMESTAMP WITHOUT TIME ZONE,
	f_ccurso VARCHAR,
	f_dmod_form VARCHAR,
	motivo_enc VARCHAR,
	f_situacao VARCHAR,
	f_carea_form DECIMAL,
	f_darea_form VARCHAR,
	revalidacao VARCHAR,
	f_vagas DECIMAL,
	f_vagas_ocupadas DECIMAL,
	motivo_recusa VARCHAR,
	sd_motivo_desemprego VARCHAR,
	apresentacao_quinzenal VARCHAR ,
	pae VARCHAR ,
	cest_superior DECIMAL,
	ano_conclusao_curso DECIMAL,
	utilizador VARCHAR ,
	cae_anterior DECIMAL,
	cod_req_rsi VARCHAR,
	f_cno_npc VARCHAR,
	f_cno_sub_ent VARCHAR,
	tipo_ocupacao VARCHAR,
	data_desemprego VARCHAR,
	id_interv_encaminh VARCHAR,
	data_subsidio VARCHAR,
	ito_id VARCHAR,
	id_interv_encaminh_origem VARCHAR,
	codigo_interv_encaminh_origem VARCHAR,
	descendentes_a_cargo VARCHAR,
	subsidio_conjuge VARCHAR,
	pos_laboral VARCHAR,
	tempo_parcial VARCHAR,
	id_conjuge VARCHAR,
	categoria_conjuge VARCHAR,
	estado_conjuge VARCHAR,
	motiv_indisp_conjuge VARCHAR,
	gestor_carreira VARCHAR,
	segmento VARCHAR,
	origem_registo_utente VARCHAR,
	data_afetacao_tecnico VARCHAR,
	data_elaboracao_ppe VARCHAR,
	pertence_ao_ppe VARCHAR,
	centroa VARCHAR,
	cpp_pretendida VARCHAR,
	tempo_pratica_ucpp VARCHAR,
	cpp_anterior VARCHAR,
	f_cno_id_estabel VARCHAR,
	enicc VARCHAR,
	gj VARCHAR,
	data_inicio_gj VARCHAR,
	data_primeira_resposta_gj VARCHAR,
	motivo_nao_sinalizacao_gj VARCHAR,
	tipo_sessao VARCHAR,
	medida_orcamental VARCHAR,
	feg VARCHAR,
	tipo_feg VARCHAR,
	rp VARCHAR,
	nce_cnacionalidade_rp VARCHAR,
	pais_residencia_estrang VARCHAR,
	grau_habilitacao_estrang VARCHAR,
	last_update_date VARCHAR
);

\COPY intervencoes from '/data/MOV_INTERVENCOES.csv' with csv header; --44,585,170

CREATE INDEX intervencoes_idx_ute_id on intervencoes(ute_id);
CREATE INDEX intervencoes_idx_ano_mes on intervencoes(ano_mes);
CREATE INDEX intervencoes_idx_data_movimento on intervencoes(data_movimento);
CREATE INDEX intervencoes_idx_estado on intervencoes(estado);
CREATE INDEX intervencoes_idx_tipo_movimento on intervencoes(tipo_movimento);
CREATE INDEX intervencoes_idx_ute_id on intervencoes(ute_id);

--table estatisticos
DROP TABLE IF EXISTS estatisticos;

CREATE TABLE estatisticos (
	ctipo_movimento DECIMAL ,
	tipo_movimento VARCHAR ,
	tabela VARCHAR,
	htipo_movimento VARCHAR
);

\COPY estatisticos from '/data/MOV_ESTATISTICOS.csv' with csv header; --72

CREATE INDEX estatisticos_idx_ctipo_movimento on estatisticos(ctipo_movimento);
CREATE INDEX estatisticos_idx_tipo_movimento on estatisticos(tipo_movimento);


--table tipos_intervencoes
DROP TABLE IF EXISTS tipos_intervencoes;

CREATE TABLE tipos_intervencoes (
	codigo_interv DECIMAL ,
	ito_eco VARCHAR ,
	dcodigo_interv VARCHAR ,
	tipo VARCHAR,
	eco_obrigatorio VARCHAR,
	cdo_obrigatorio VARCHAR,
	ppe_obrigatorio VARCHAR,
	cdo_act_obrigatorio VARCHAR,
	dfa_obrigatoria VARCHAR,
	sso_obrigatorio VARCHAR,
	sso_nulo VARCHAR,
	possi_eco_simultaneo VARCHAR,
	accao_form_obrigatoria VARCHAR,
	grupo_sieg DECIMAL,
	descricao VARCHAR,
	risco_elevado VARCHAR,
	risco_medio VARCHAR,
	risco_baixo VARCHAR,
	tipo_movimento DECIMAL
);

\COPY tipos_intervencoes from '/data/TIPOS_INTERVENCOES.csv' with csv header; --484

CREATE INDEX tipos_intervencoes_idx_codigo_interv on tipos_intervencoes(codigo_interv);
CREATE INDEX tipos_intervencoes_idx_dcodigo_interv on tipos_intervencoes(dcodigo_interv);
CREATE INDEX tipos_intervencoes_idx_tipo on tipos_intervencoes(tipo);



--table resultado_intervencaoes
DROP TABLE IF EXISTS resultado_intervencoes;

CREATE TABLE resultado_intervencoes (
	cresultado DECIMAL,
	dresultado VARCHAR,
	hresultado VARCHAR,
	codigo_interv DECIMAL,
	dresultado_collapsed VARCHAR
);

CREATE INDEX resultado_intervencoes_cresultado on resultado_intervencoes(cresultado);
CREATE INDEX resultado_intervencoes_dresultado on resultado_intervencoes(dresultado);
CREATE INDEX resultado_intervencoes_hresultado on resultado_intervencoes(hresultado);
CREATE INDEX resultado_intervencoes_codigo_interv on resultado_intervencoes(codigo_interv);

\COPY resultado_intervencoes from '/data/RESULTADO_INTERVENCOES.csv' with csv header; --2652

DROP TABLE IF EXISTS resultado_convocados;

--table resultado_convocados
CREATE TABLE resultado_convocados (
	resultado DECIMAL,
	dresultado_convocatoria VARCHAR,
	resultado_conv_collapsed VARCHAR,
	hresultado_convocatoria VARCHAR
);

\COPY resultado_convocados from '/data/RESULTADO_CONVOCADOS.csv' with csv header; --23

--table resultado_apresentacaoes
DROP TABLE IF EXISTS resultado_apresentacoes;

CREATE TABLE resultado_apresentacoes (
	resultado_apres DECIMAL,
	dresultado_apres VARCHAR,
	resultado_apres_collapsed VARCHAR,
	hresultado_apres VARCHAR
);

\COPY resultado_apresentacoes from '/data/RESULTADO_APRESENTACOES.csv' with csv header;

--table nacionalidade
DROP TABLE IF EXISTS nacionalidade;

CREATE TABLE nacionalidade (
	cnacionalidade VARCHAR,
	cnacionalidade_collapsed VARCHAR,
	hnacionalidade VARCHAR ,
	dnacionalidade VARCHAR
);

\COPY nacionalidade from '/data/NACIONALIDADE.csv' with csv header; --200

--table motivos_suspensao_cessacao_subsidio
DROP TABLE IF EXISTS motivos_suspensao_cessacao_subsidio;

CREATE TABLE motivos_suspensao_cessacao_subsidio (
	cmotivo VARCHAR,
	motivo VARCHAR,
	agregacao VARCHAR,
	estado VARCHAR,
	hmotivo VARCHAR,
	estado_code DECIMAL
);

\COPY motivos_suspensao_cessacao_subsidio from '/data/MOTIVOS_SUSPENSAO_CESSACAO_SUBSIDIO.csv' with csv header; --124

--table motivos_inscricao
DROP TABLE IF EXISTS motivos_inscricao;

CREATE TABLE motivos_inscricao (
	cmotivo_inscricao DECIMAL ,
	dmotivo_inscricao VARCHAR ,
	ind_mot_insc DECIMAL ,
	descricao VARCHAR,
	hmotivo_inscricao VARCHAR
);

\COPY motivos_inscricao from '/data/MOTIVOS_INSCRICAO.csv' with csv header; --29

--table motivos_anulacao
DROP TABLE IF EXISTS motivos_anulacao;

CREATE TABLE motivos_anulacao (
	cmotivo_anulacao DECIMAL ,
	dmotivo_anulacao VARCHAR ,
	motivos_anulacao_agg VARCHAR,
	motivos_anul_agg_short VARCHAR,
	hmotivo_anulacao VARCHAR
);

\COPY motivos_anulacao from '/data/MOTIVOS_ANULACAO.csv' with csv header; --51

--table freguesia_nuts
DROP TABLE IF EXISTS freguesia_nuts;

CREATE TABLE freguesia_nuts (
	cnutsiii VARCHAR,
	dnutsiii VARCHAR,
	cfreguesia VARCHAR,
	dfreguesia VARCHAR
);

\COPY freguesia_nuts from '/data/FREGUESIA_NUTS.csv' with csv header; --6931

--table cae_correspondence
DROP TABLE IF EXISTS cae_correspondence;

CREATE TABLE cae_correspondence (
	cae_divisao DECIMAL ,
	cae_seccao VARCHAR ,
	hcae VARCHAR
);

\COPY cae_correspondence from '/data/CAE_CORRESPONDENCE.csv' with csv header; --89

--table get_utentes
DROP TABLE IF EXISTS utentes;

CREATE TABLE utentes (
	id DECIMAL ,
	estado VARCHAR,
	motivo_candidatura DECIMAL,
	motivo_anulacao DECIMAL,
	data_candidatura TIMESTAMP WITHOUT TIME ZONE,
	a_tempo VARCHAR,
	natureza VARCHAR,
	carteira_profissional VARCHAR,
	formacao_profissional VARCHAR,
	salario DECIMAL,
	moeda VARCHAR,
	tempo_ultimo_cnp DECIMAL,
	divulgacao_pretendida VARCHAR,
	qualificacao DECIMAL,
	data_nascimento TIMESTAMP WITHOUT TIME ZONE,
	estado_civil VARCHAR ,
	sexo VARCHAR ,
	pessoas_cargo DECIMAL,
	data_inscricao TIMESTAMP WITHOUT TIME ZONE,
	carta_conducao VARCHAR,
	ppe VARCHAR ,
	situacao_militar VARCHAR,
	transporte_proprio VARCHAR,
	data_nao_reinscricao TIMESTAMP WITHOUT TIME ZONE,
	ute_type VARCHAR ,
	ccentro DECIMAL ,
	chabilitacao_escolar VARCHAR ,
	cnp_utente DECIMAL,
	cnacionalidade VARCHAR ,
	cfreguesia VARCHAR ,
	cdeficiencia DECIMAL ,
	freguesia_outra VARCHAR,
	cae DECIMAL,
	cnp_principal DECIMAL,
	ccategoria DECIMAL,
	data_primeira_candidatura TIMESTAMP WITHOUT TIME ZONE,
	salario_pretendido DECIMAL,
	moeda_salario_pretendido VARCHAR,
	freguesia_ultima_cnp VARCHAR,
	ppe_anterior VARCHAR ,
	motivo_inscricao_utente DECIMAL ,
	tuc DECIMAL ,
	estabelecimento VARCHAR,
	desc_motivo_inscricao VARCHAR,
	desc_motivo_anulacao VARCHAR,
	data_anulacao TIMESTAMP WITHOUT TIME ZONE,
	sub VARCHAR ,
	def VARCHAR ,
	area_formacao DECIMAL,
	area_curso VARCHAR,
	origem_insercao VARCHAR,
	origem_candidatura VARCHAR,
	rsi VARCHAR,
	con_naturalidade DECIMAL,
	ncd_naturalidade VARCHAR,
	pae VARCHAR ,
	motivo_indisponibilidade DECIMAL,
	data_fim_indisponivel TIMESTAMP WITHOUT TIME ZONE,
	ano_conclusao_curso DECIMAL,
	feg VARCHAR,
	ac VARCHAR,
	tipo_feg DECIMAL,
	conjuge_inscrito VARCHAR,
	sigo VARCHAR,
	tipo_ocupacao DECIMAL,
	data_inicio_ocupacao TIMESTAMP WITHOUT TIME ZONE,
	data_fim_ocupacao TIMESTAMP WITHOUT TIME ZONE,
	categoria_ant DECIMAL,
	tie DECIMAL,
	ascendentes_a_cargo DECIMAL ,
	descendentes_a_cargo DECIMAL,
	agregado_monoparental VARCHAR,
	utilizador VARCHAR,
	data_atrib_gc TIMESTAMP WITHOUT TIME ZONE,
	coeficiente_profiling DECIMAL,
	segmento_atribuido VARCHAR,
	segmento_automatico VARCHAR,
	requerer_sd VARCHAR,
	cpp_principal DECIMAL,
	cpp_utente DECIMAL,
	tempo_ultimo_cpp DECIMAL,
	freguesia_ultima_cpp VARCHAR,
	gj VARCHAR,
	data_inicio_gj TIMESTAMP WITHOUT TIME ZONE,
	data_primeira_resposta_gj TIMESTAMP WITHOUT TIME ZONE,
	motivo_nao_sinalizacao_gj DECIMAL,
	motivo_fim_gj DECIMAL,
	data_fim_gj TIMESTAMP WITHOUT TIME ZONE,
	gj_ant VARCHAR,
	data_inicio_gj_ant TIMESTAMP WITHOUT TIME ZONE,
	primeira_resposta_gj DECIMAL,
	creation_date VARCHAR,
	last_update_date TIMESTAMP WITHOUT TIME ZONE,
	prim_resp_gj_inicial DECIMAL,
	data_prim_resp_gj_inicial TIMESTAMP WITHOUT TIME ZONE,
	data_inicio_agreg TIMESTAMP WITHOUT TIME ZONE,
	n_agregado DECIMAL,
	n_desempregados DECIMAL,
	n_inativos DECIMAL,
	n_criancas DECIMAL,
	cv VARCHAR ,
	validador VARCHAR,
	util_tecnico_manual VARCHAR,
	tempo_pratica DECIMAL
);

\COPY utentes from '/data/GET_UTENTES.csv' with csv header; --5,667,885

CREATE INDEX utentes_idx_id on utentes(id);

--table get_ppe
DROP TABLE IF EXISTS action_plans;

CREATE TABLE action_plans (
	iti_id DECIMAL ,
	estado_iti VARCHAR ,
	ute_id DECIMAL ,
	data_iti TIMESTAMP WITHOUT TIME ZONE,
	numero_iti DECIMAL ,
	responsavel VARCHAR ,
	data_revisao TIMESTAMP WITHOUT TIME ZONE,
	numero_etapa DECIMAL ,
	codigo DECIMAL ,
	estado_etapa VARCHAR ,
	eco_id VARCHAR,
	data_encaminhamento VARCHAR,
	resultado_eco VARCHAR,
	data_resultado_eco VARCHAR,
	ito_id DECIMAL,
	data_intervencao TIMESTAMP WITHOUT TIME ZONE,
	resultado_ito DECIMAL,
	data_resultado_ito TIMESTAMP WITHOUT TIME ZONE
);

\COPY action_plans from '/data/GET_PPE.csv' with csv header;

CREATE INDEX action_plans_idx_codidgo on action_plans(codigo);

--table get_ofertas
DROP TABLE IF EXISTS get_ofertas;

CREATE TABLE get_ofertas (
	estado VARCHAR ,
	salario DECIMAL,
	moeda VARCHAR,
	tipo_salario VARCHAR,
	transporte_proprio VARCHAR,
	data_inicio TIMESTAMP WITHOUT TIME ZONE,
	data_comunicacao TIMESTAMP WITHOUT TIME ZONE,
	natureza_emprego VARCHAR ,
	a_tempo VARCHAR ,
	duracao DECIMAL,
	idade_min DECIMAL,
	idade_max DECIMAL,
	carta_conducao VARCHAR,
	formacao_profissional VARCHAR,
	data_apresentacao TIMESTAMP WITHOUT TIME ZONE,
	saldo_postos DECIMAL ,
	data_validade TIMESTAMP WITHOUT TIME ZONE,
	qualificacoes DECIMAL,
	data_insercao TIMESTAMP WITHOUT TIME ZONE,
	nr_oferta DECIMAL ,
	ccentro DECIMAL ,
	cnp DECIMAL ,
	habilitacao_minima VARCHAR,
	habilitacao_maxima VARCHAR,
	cnacionalidade VARCHAR,
	nivel_divulgacao DECIMAL ,
	data_ultima_divulgacao TIMESTAMP WITHOUT TIME ZONE,
	bde_freguesia VARCHAR ,
	bde_cae DECIMAL ,
	bde_nr_pessoas_servico DECIMAL ,
	area_recrutamento VARCHAR,
	centro_ctn_n_p VARCHAR,
	centro_ctn DECIMAL,
	carteira_profissional VARCHAR,
	sub_refeicao VARCHAR,
	valor_sub_refeicao DECIMAL,
	sub_turno VARCHAR,
	valor_sub_turno DECIMAL,
	sub_transporte VARCHAR,
	valor_sub_transporte DECIMAL,
	origem VARCHAR ,
	tempo_pratica_min DECIMAL,
	tempo_pratica_max VARCHAR,
	tipo_oferta_lse VARCHAR ,
	aceitar_bec VARCHAR,
	motivo_suspensao VARCHAR,
	data_suspensao TIMESTAMP WITHOUT TIME ZONE,
	valida_apres_internet VARCHAR,
	pe2012 VARCHAR,
	interesse_estrategico VARCHAR,
	cae_ett VARCHAR,
	freguesia_ett VARCHAR,
	concurso_publico_ett VARCHAR,
	regime_horario VARCHAR,
	cedencia_ett VARCHAR,
	reducao_tsu VARCHAR,
	nivel_intermediacao DECIMAL,
	tipo_oferta VARCHAR ,
	valor_diario_viagens VARCHAR,
	pagamento_viagens VARCHAR,
	experiencia_ant_exigida VARCHAR,
	carta_conducao_necessaria VARCHAR,
	apoio_alojamento VARCHAR,
	valor_diario_alojamento VARCHAR,
	startup VARCHAR,
	tsu45 VARCHAR,
	me2013 VARCHAR,
	processo_recup_empresas VARCHAR,
	reembolso_tsu VARCHAR,
	cpp DECIMAL,
	me2014 VARCHAR,
	eao VARCHAR,
	e_mais VARCHAR,
	num_postos_trabalho_ini VARCHAR,
	consentimento_eures VARCHAR,
	recrutamento_eures VARCHAR,
	creation_date VARCHAR,
	last_update_date TIMESTAMP WITHOUT TIME ZONE
);

\COPY get_ofertas from '/data/GET_OFERTAS.csv' with csv header; --1,722,588
