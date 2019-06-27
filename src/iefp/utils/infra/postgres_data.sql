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

CREATE INDEX ofertas_idx_nr_oferta on ofertas(nr_oferta);

\copy ofertas from 'EMP_OFERTAS.csv' with csv header; --

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

CREATE INDEX pedidos_idx_ute_id on pedidos(ute_id);
CREATE INDEX pedidos_idx_data_movimento on pedidos(data_movimento);
CREATE INDEX pedidos_idx_ute_id_data_movimento on pedidos(ute_id, data_movimento);


\copy pedidos from 'emp_pedidos.csv' with csv header; --37,317,447

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

CREATE INDEX apresentados_idx_ute_id on apresentados(ute_id);
CREATE INDEX apresentados_idx_nr_oferta on apresentados(nr_oferta);
CREATE INDEX apresentados_idx_data_movimento on apresentados(data_movimento);

\COPY apresentados from 'MOV_APRESENTADOS.csv' with csv header; --13,989,614

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


CREATE INDEX convocados_idx_ute_id on convocados(ute_id);
CREATE INDEX convocados_idx_nr_oferta on convocados(nr_oferta);
CREATE INDEX convocados_idx_data_movimento on convocados(data_movimento);

\COPY  convocados from 'MOV_CONVOCADOS.csv' with csv header; --38,498,895

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
	centro_np DECIMAL,
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

\COPY intervencoes from 'MOV_INTERVENCOES.csv' with csv header; --44,585,170

--intevenciones 44,585,171

--table estatisticos
DROP TABLE IF EXISTS estatisticos;

CREATE TABLE estatisticos (
	ctipo_movimento DECIMAL ,
	tipo_movimento VARCHAR ,
	tabela VARCHAR,
	htipo_movimento VARCHAR
);

\COPY estatisticos from 'MOV_ESTATISTICOS.csv' with csv header; --72

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

CREATE INDEX intervencoes_idx_codigo_interv on tipos_intervencoes(codigo_interv);
CREATE INDEX intervencoes_idx_dcodigo_interv on tipos_intervencoes(dcodigo_interv);
CREATE INDEX intervencoes_idx_tipo on tipos_intervencoes(tipo);

\COPY tipos_intervencoes from 'TIPOS_INTERVENCOES.csv' with csv header; --484

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

\COPY resultado_intervencoes from 'RESULTADO_INTERVENCOES.csv' with csv header; --2652

DROP TABLE IF EXISTS resultado_convocados;

--table resultado_convocados
CREATE TABLE resultado_convocados (
	resultado DECIMAL,
	dresultado_convocatoria VARCHAR,
	resultado_conv_collapsed VARCHAR,
	hresultado_convocatoria VARCHAR
);

\COPY resultado_convocados from 'RESULTADO_CONVOCADOS.csv' with csv header; --23

--table resultado_apresentacaoes
DROP TABLE IF EXISTS resultado_apresentacoes;

CREATE TABLE resultado_apresentacoes (
	resultado_apres DECIMAL,
	dresultado_apres VARCHAR,
	resultado_apres_collapsed VARCHAR,
	hresultado_apres VARCHAR
);

\COPY resultado_apresentacoes from 'RESULTADO_APRESENTACOES.csv' with csv header;

--table nacionalidade
DROP TABLE IF EXISTS nacionalidade;

CREATE TABLE nacionalidade (
	cnacionalidade VARCHAR,
	cnacionalidade_collapsed VARCHAR,
	hnacionalidade VARCHAR NOT NULL,
	dnacionalidade VARCHAR NOT NULL
);

\COPY nacionalidade from 'NACIONALIDADE.csv' with csv header; --200

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

\COPY motivos_suspensao_cessacao_subsidio from 'MOTIVOS_SUSPENSAO_CESSACAO_SUBSIDIO.csv' with csv header; --124

--table motivos_inscricao
DROP TABLE IF EXISTS motivos_inscricao;

CREATE TABLE motivos_inscricao (
	cmotivo_inscricao DECIMAL NOT NULL,
	dmotivo_inscricao VARCHAR NOT NULL,
	ind_mot_insc DECIMAL NOT NULL,
	descricao VARCHAR,
	hmotivo_inscricao VARCHAR NOT NULL
);

\COPY motivos_inscricao from 'MOTIVOS_INSCRICAO.csv' with csv header; --29

--table motivos_anulacao
DROP TABLE IF EXISTS motivos_anulacao;

CREATE TABLE motivos_anulacao (
	cmotivo_anulacao DECIMAL NOT NULL,
	dmotivo_anulacao VARCHAR NOT NULL,
	motivos_anulacao_agg VARCHAR,
	motivos_anul_agg_short VARCHAR,
	hmotivo_anulacao VARCHAR NOT NULL
);

\COPY motivos_anulacao from 'MOTIVOS_ANULACAO.csv' with csv header; --51

--table freguesia_nuts
DROP TABLE IF EXISTS freguesia_nuts;

CREATE TABLE freguesia_nuts (
	cnutsiii VARCHAR,
	dnutsiii VARCHAR,
	cfreguesia VARCHAR,
	dfreguesia VARCHAR
);

\COPY freguesia_nuts from 'FREGUESIA_NUTS.csv' with csv header; --6931

--table cae_correspondence
DROP TABLE IF EXISTS cae_correspondence;

CREATE TABLE cae_correspondence (
	cae_divisao DECIMAL NOT NULL,
	cae_seccao VARCHAR NOT NULL,
	hcae VARCHAR NOT NULL
);

\COPY cae_correspondence from 'CAE_CORRESPONDENCE.csv' with csv header; --89
