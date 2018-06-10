-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 06-06-2018 a las 12:48:47
-- Versión del servidor: 5.7.22-0ubuntu0.16.04.1
-- Versión de PHP: 7.0.28-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `CABD`
--
CREATE DATABASE IF NOT EXISTS `CABD` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `CABD`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_app`
--

CREATE TABLE `app_app` (
  `id` int(11) NOT NULL,
  `taskcode` varchar(100) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `citation` longtext,
  `image` varchar(100) DEFAULT NULL,
  `command` varchar(100) NOT NULL,
  `description` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_app`:
--

--
-- Volcado de datos para la tabla `app_app`
--

INSERT INTO `app_app` (`id`, `taskcode`, `name`, `citation`, `image`, `command`, `description`) VALUES
(1, 'sma3sv2', 'Sma3s v2', 'Sma3s is licensed under a Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.', 'app/sma3s.png', 'sma3s_v2.exe', 'Annotate proteomes & transcriptomes'),
(2, 'prodigal', 'Prodigal', '', 'app/prodigal.png', 'prodigal.windows.exe', 'Prediction of protein coding genes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_appcompatibility`
--

CREATE TABLE `app_appcompatibility` (
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_appcompatibility`:
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_app_app_compatibility`
--

CREATE TABLE `app_app_app_compatibility` (
  `id` int(11) NOT NULL,
  `from_app_id` int(11) NOT NULL,
  `to_app_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_app_app_compatibility`:
--   `from_app_id`
--       `app_app` -> `id`
--   `to_app_id`
--       `app_app` -> `id`
--

--
-- Volcado de datos para la tabla `app_app_app_compatibility`
--

INSERT INTO `app_app_app_compatibility` (`id`, `from_app_id`, `to_app_id`) VALUES
(2, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_company`
--

CREATE TABLE `app_company` (
  `description` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_company`:
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_imageslideshow`
--

CREATE TABLE `app_imageslideshow` (
  `id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_imageslideshow`:
--

--
-- Volcado de datos para la tabla `app_imageslideshow`
--

INSERT INTO `app_imageslideshow` (`id`, `image`, `title`) VALUES
(4, 'index/ab.png', ''),
(5, 'index/workflow.png', ''),
(6, 'index/enrichment.png', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_mycompany`
--

CREATE TABLE `app_mycompany` (
  `id` int(11) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `address` longtext NOT NULL,
  `phone` varchar(9) NOT NULL,
  `email` varchar(254) NOT NULL,
  `citations` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_mycompany`:
--

--
-- Volcado de datos para la tabla `app_mycompany`
--

INSERT INTO `app_mycompany` (`id`, `logo`, `name`, `address`, `phone`, `email`, `citations`) VALUES
(2, 'index/logo.jpg', 'GGAFE, Gene & Genome Annotation For Everybody', 'Universidad Pablo de Olavide Ctra/ Utrera, Km. 1 41013', '954348652', 'daniel.tfg.cabd@gmail.com', 'Please cite our paper if you use this website. This will help the Pathview project in return. - Luo W, Pant G, Bhavnasi YK, Blanchard SG, Brouwer C. Pathview Web: user friendly pathway visualization and data integration. Nucleic Acids Res, 2017, Web Server issue, doi: 10.1093/ nar/gkx372- Luo W, Brouwer C. Pathview: an R/Biocondutor package for pathway-based data integration and visualization. Bioinformatics, 2013, 29(14):1830-1831, doi: 10.1093/bioinformatics/btt285Please also cite GAGE paper if you are doing pathway analysis besides visualization, i.e. Pathway Selection set to Auto on the New Analysis page.- Luo W, Friedman M, etc. GAGE: generally applicable gene set enrichment for pathway analysis. BMC Bioinformatics, 2009, 10, pp. 161, doi: 10.1186/1471-2105-10-161');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_paraminputoption`
--

CREATE TABLE `app_paraminputoption` (
  `id` int(11) NOT NULL,
  `value` varchar(100) NOT NULL,
  `select_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_paraminputoption`:
--   `select_id`
--       `app_paramsinputselect` -> `id`
--

--
-- Volcado de datos para la tabla `app_paraminputoption`
--

INSERT INTO `app_paraminputoption` (`id`, `value`, `select_id`) VALUES
(2, 'a', 3),
(3, 'b', 3),
(4, 'c', 4),
(5, 'd', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_paramsinput`
--

CREATE TABLE `app_paramsinput` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `state` varchar(15) NOT NULL,
  `allowed_format` varchar(100) NOT NULL,
  `app_id` int(11) NOT NULL,
  `is_required` tinyint(1) NOT NULL,
  `value` varchar(100) NOT NULL,
  `info` longtext NOT NULL,
  `option` varchar(100) NOT NULL,
  `is_file_input` tinyint(1) NOT NULL,
  `is_file_output` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_paramsinput`:
--   `app_id`
--       `app_app` -> `id`
--

--
-- Volcado de datos para la tabla `app_paramsinput`
--

INSERT INTO `app_paramsinput` (`id`, `name`, `state`, `allowed_format`, `app_id`, `is_required`, `value`, `info`, `option`, `is_file_input`, `is_file_output`) VALUES
(1, 'Gene Data', 'file', '.fasta', 1, 1, '', 'Input file, allowed format .fasta', '-i', 1, 0),
(3, 'd', 'read', '', 1, 1, 'uniprot_Bacillus_subtilis.fasta', '', '-d', 0, 0),
(4, 'Gene Data', 'file', '.fasta', 2, 1, '', 'Input file, allowed format .fasta', '-i', 1, 0),
(5, 'Output Data', 'file', '.fasta', 2, 1, '', 'Output file, allowed format .fasta', '-a', 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_paramsinputfile`
--

CREATE TABLE `app_paramsinputfile` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `allowed_format` varchar(100) NOT NULL,
  `option` varchar(10) NOT NULL,
  `info` longtext NOT NULL,
  `app_id` int(11) NOT NULL,
  `file_input` varchar(100) NOT NULL,
  `file_output` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_paramsinputfile`:
--   `app_id`
--       `app_app` -> `id`
--

--
-- Volcado de datos para la tabla `app_paramsinputfile`
--

INSERT INTO `app_paramsinputfile` (`id`, `name`, `type`, `allowed_format`, `option`, `info`, `app_id`, `file_input`, `file_output`) VALUES
(1, 'Gene Data', 'input', '.fasta', '-i', 'Input file, allowed format .fasta', 1, '', ''),
(2, 'Gene Data', 'input', '.fasta', '-i', 'Input file, allowed format .fasta', 2, '', ''),
(3, 'Output Data', 'output', '.fasta', '-a', 'Output file, allowed format .fasta', 2, '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_paramsinputselect`
--

CREATE TABLE `app_paramsinputselect` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `option` varchar(10) NOT NULL,
  `info` longtext NOT NULL,
  `app_id` int(11) NOT NULL,
  `value` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_paramsinputselect`:
--   `app_id`
--       `app_app` -> `id`
--

--
-- Volcado de datos para la tabla `app_paramsinputselect`
--

INSERT INTO `app_paramsinputselect` (`id`, `name`, `option`, `info`, `app_id`, `value`) VALUES
(3, 'Select 1', 'ssss', 'sssss', 1, ''),
(4, 'Select 2', 'eeeee', 'eeeeee', 1, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_paramsinputtext`
--

CREATE TABLE `app_paramsinputtext` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `value` varchar(100) NOT NULL,
  `option` varchar(10) NOT NULL,
  `info` longtext NOT NULL,
  `app_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_paramsinputtext`:
--   `app_id`
--       `app_app` -> `id`
--

--
-- Volcado de datos para la tabla `app_paramsinputtext`
--

INSERT INTO `app_paramsinputtext` (`id`, `name`, `value`, `option`, `info`, `app_id`) VALUES
(2, 'Texto1', '', '-t', 'fdfdsfdsfds', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_profile`
--

CREATE TABLE `app_profile` (
  `id` int(11) NOT NULL,
  `institution` varchar(100) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_profile`:
--   `user_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `app_profile`
--

INSERT INTO `app_profile` (`id`, `institution`, `user_id`) VALUES
(4, 'UPO', 4),
(6, 'UPO', 6),
(7, 'Universidad Pablo de Olavide', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_section`
--

CREATE TABLE `app_section` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `subsection_id` int(11) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_section`:
--   `app_id`
--       `app_app` -> `id`
--   `subsection_id`
--       `app_section` -> `id`
--

--
-- Volcado de datos para la tabla `app_section`
--

INSERT INTO `app_section` (`id`, `title`, `subsection_id`, `app_id`, `description`) VALUES
(1, 'Overview', NULL, 1, 'Sma3s (Sequence massive annotator using 3 modules) is an easy-to-use tool for high throughput annotation that provides both accuracy and broad applicability for different kinds of sequence datasets such as proteomes or transcriptomes.\r\n\r\nBiological sequence annotation is the process of associating biological information to sequences of interest. Annotations can include the potential function, cellular localization, biological process or protein structure of a given sequence, and is of special interest for genomics projects, gene-expression experiments and many other emerging areas of research.\r\n\r\nSma3s is a tool for this important area, which is especially focused on the massive annotation of sequences from any kind of gene library or genome. It provides high levels of prediction accuracy (higher than 80%) with minimal manual input and low computational resource requirements. It is composed of three integrative modules that  annotate unknown sequences with increasing difficulty.  All three modules use a preliminary exhaustive BLAST search as their starting point, and together generate annotations that are both highly sensitive and specific.\r\n\r\nFinally, Sma3s offers results in files that can be easily managed and opened with a spreadsheet program.'),
(2, 'What do you need for annotating a sequence dataset?', NULL, 1, 'Sma3s has low computing requirements and can be used on virtually any computer. It is written in Perl language and you need its interpreter (http://www.perl.com), which is preinstalled in Linux and Mac OS X (in Windows it will not be necessary). Additionally, you need to install the Blast+ package for your operating system.\r\n\r\nFinally, you will need our Sma3s program:\r\n\r\n>>> Sma3s_v2.pl <<< (see Creative Commons license)\r\n\r\nTo annotate your sequence dataset, you only need the following files:\r\n\r\nYour query sequences in multi-FASTA format,\r\nThe reference database, which you can download from our server: http://www.bioinfocabd.upo.es/sma3s/db/\r\nUsual command line for annotating proteomes:\r\n./sma3s.pl -i query_dataset.fasta -d uniref90.fasta -goslim\r\n\r\nUsual command line for annotating transcriptomes:\r\n ./sma3s.pl -i query_dataset.fasta -d uniref90.fasta -nucl -goslim\r\n\r\nRun "sma3s_v2.pl --help" for help with these and other advanced parameters.\r\n\r\nAlternatively, you can use Sma3s with the whole UniProt database, if you are interested in a more sensitive, though more slowly, annotation. To do that, you must download a .dat file from UniProt (ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/), and install the Blast Legacy package (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy/).'),
(3, 'What\'s new', NULL, 1, 'Sma3s allows high-throughput annotation analysis to non-specialist users. These are the improvements for the new Sma3s release 2:\r\n\r\nPerformance: the algorithm is now more exhaustive and accurate\r\n\r\nIt offers a combined annotation from the 3 available modules, giving preference to manually curated sequences from the database.\r\n\r\nBoth the assigned gene name and description come from the most informative sequence.\r\n\r\nThe module 2 uses the Rost equation and takes in account the ortholog with the best annotation.\r\n\r\nIt takes automatic parameters for improving transcriptome annotations.\r\n\r\nUsability: it requires both low knowledge and computing requirements\r\n\r\nIt only requires the external Blast+ package.\r\n\r\nIt can be easily run in Linux, Windows and Mac.\r\n\r\nA reference database is provided to make easier the annotation.\r\n\r\nOutput utility: the result includes a summary useful to create figures\r\n\r\nA summary of the whole annotation is given, with the number of annotated sequences and a brief about found functional classes which can be used to create article figures.\r\n\r\nEC numbers are added to the annotation, and the GO terms are separately shown for each category.\r\n\r\nGeneric GO Slim can be added to the annotation.\r\n\r\nThe sequences used for the annotation can be reported, and the unannotated sequences can be discarded from the final report.\r\n\r\nQuality: the user can select only quality predictions\r\n\r\nA quality annotation can be performed by using GO and UniProt evidence codes.\r\n\r\nNon-informative annotation are avoided, as well as database sequences without any GO term and UniProt keyword.\r\n\r\nRun time: the processing time has decreased and it can be easily run in a personal computer\r\n\r\nThe similarity search by Blast, which is the most demanding processing time step, can be run in a multi-thread way.\r\n\r\nIt uses the non-redundant database UniRef90 which reduces the processing time, but keeping a high sensitivity.\r\n\r\nWhen using UniRef90, the clustering step for removing redundancy can be avoided.\r\n\r\nAll of this gets a 4-fold processing increase.\r\n\r\nSma3s old release'),
(4, 'References', NULL, 1, 'Please cite the use of Sma3s with the last reference:\r\n\r\nAntonio Muñoz-Mérida, Enrique Viguera, M. Gonzalo Claros, Oswaldo Trelles, Antonio J. Pérez-Pulido. Sma3s: a three-step modular annotator for large sequence datasets. DNA Research 2014 Aug;21(4):341-53.\r\nCarlos S. Casimiro-Soriguer, Antonio Muñoz-Mérida, Antonio J. Pérez-Pulido. Sma3s: a universal tool for easy functional annotation of proteomes and transcriptomes. Proteomics 2017, in press.\r\nSma3s have been widely used and cited in the literature.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_task`
--

CREATE TABLE `app_task` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `state` varchar(15) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `file_input` varchar(100) NOT NULL,
  `file_output` varchar(100) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `taskcode` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `app_task`:
--   `app_id`
--       `app_app` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

--
-- Volcado de datos para la tabla `app_task`
--

INSERT INTO `app_task` (`id`, `name`, `state`, `creation_date`, `file_input`, `file_output`, `app_id`, `user_id`, `taskcode`) VALUES
(18, 'sma3s_v2.exe ssss a -t vsvvvv eeeee c -i Docker.odt', 'pending', '2018-05-21 21:59:23.229625', 'files/input/Docker_nzFoLFr.odt', '', 1, 6, 'Sma3s v2'),
(19, 'sma3s_v2.exe ssss a -t vsvvvv eeeee c -i Docker.odt', 'pending', '2018-05-21 22:16:16.475856', 'files/input/Docker_ZmrNP0H.odt', '', 1, 6, 'Sma3s v2'),
(20, 'sma3s_v2.exe ssss a -t yyyyyyyyy eeeee c -i Docker.odt', 'pending', '2018-05-21 22:17:15.816487', 'files/input/Docker_LzLtV40.odt', '', 1, 6, 'Sma3s v2'),
(21, 'sma3s_v2.exe ssss a -t lllllllll eeeee c -i Docker.odt', 'pending', '2018-05-21 22:23:36.209472', 'files/input/Docker_AxdyKBf.odt', '', 1, 6, 'Sma3s v2'),
(22, 'sma3s_v2.exe ssss a -t horar eeeee d -i horario.csv', 'pending', '2018-05-23 14:40:10.285385', 'files/input/horario.csv', '', 1, 6, 'Sma3s v2'),
(23, 'sma3s_v2.exe ssss a -t ddd eeeee c -i horario.csv', 'pending', '2018-05-23 14:43:55.446546', 'files/input/horario_WChaCip.csv', '', 1, 6, 'Sma3s v2'),
(24, 'sma3s_v2.exe ssss a -t ll eeeee c -i 24355sc.csv', 'pending', '2018-05-23 14:51:34.030944', 'files/input/24355sc_D5OLDAP.csv', '', 1, 6, 'Sma3s v2'),
(25, 'sma3s_v2.exe ssss a -t bbn eeeee c -i 24355sc.csv', 'pending', '2018-05-23 14:56:29.075441', 'files/input/24355sc_CW43Hcp.csv', '', 1, 6, 'Sma3s v2'),
(26, 'sma3s_v2.exe ssss a -t gggg eeeee c -i index.html', 'pending', '2018-05-23 14:57:21.397778', 'files/input/index.html', '', 1, 6, 'Sma3s v2'),
(27, 'sma3s_v2.exe ssss a -t ffff eeeee c -i Cursos.csv', 'pending', '2018-05-23 15:00:22.748544', 'files/input/Cursos.csv', '', 1, 6, 'Sma3s v2'),
(28, 'sma3s_v2.exe ssss a -t vvvv eeeee c -i 24355sc.csv', 'pending', '2018-05-23 15:19:43.800217', 'files/input/24355sc_RUEkaqs.csv', '', 1, 6, 'Sma3s v2'),
(29, 'sma3s_v2.exe ssss a -t vvvv eeeee c -i 24355sc.csv', 'pending', '2018-05-23 15:30:10.699714', 'files/input/24355sc_9jdQls7.csv', '', 1, 6, 'Sma3s v2'),
(30, 'sma3s_v2.exe ssss a -t v eeeee c -i horario.csv', 'pending', '2018-05-23 15:30:51.772014', 'files/input/horario_QMxfq82.csv', '', 1, 6, 'Sma3s v2'),
(31, 'sma3s_v2.exe ssss a -t vv eeeee c -i horario.csv', 'pending', '2018-05-23 15:31:44.216912', 'files/input/horario_W4nqwek.csv', '', 1, 6, 'Sma3s v2'),
(32, 'sma3s_v2.exe ssss a -t vvxx eeeee c -i 24355sc.csv', 'pending', '2018-05-23 15:33:07.790598', 'files/input/24355sc.csv', '', 1, 6, 'Sma3s v2'),
(33, 'sma3s_v2.exe ssss a -t nnn eeeee c -i Cursos.csv', 'pending', '2018-05-23 15:40:16.912544', 'files/input/Cursos.csv', '', 1, 6, 'Sma3s v2'),
(34, 'sma3s_v2.exe ssss a -t nnn eeeee c -i Cursos.csv', 'pending', '2018-05-23 15:49:18.710478', 'files/input/Cursos_KSEvbwc.csv', '', 1, 6, 'Sma3s v2'),
(35, 'sma3s_v2.exe ssss a -t nnn eeeee c -i Cursos.csv', 'pending', '2018-05-23 15:54:20.142212', 'files/input/Cursos_BdB5Yk8.csv', '', 1, 6, 'Sma3s v2'),
(36, 'sma3s_v2.exe ssss a -t nnn eeeee c -i Cursos.csv', 'pending', '2018-05-23 15:54:31.321794', 'files/input/Cursos_9UJ8p0C.csv', '', 1, 6, 'Sma3s v2'),
(37, 'sma3s_v2.exe ssss a -t bbbb eeeee c -i index.html', 'pending', '2018-05-23 15:54:49.149072', 'files/input/index_svpmzhp.html', '', 1, 6, 'Sma3s v2'),
(38, 'sma3s_v2.exe ssss a -t b eeeee c -i horario.csv', 'pending', '2018-05-23 15:55:57.166875', 'files/input/horario.csv', '', 1, 6, 'Sma3s v2'),
(39, 'sma3s_v2.exe ssss a -t b eeeee c -i horario.csv', 'pending', '2018-05-23 15:57:08.503712', 'files/input/horario_5EMoOZk.csv', '', 1, 6, 'Sma3s v2'),
(40, 'sma3s_v2.exe ssss a -t b eeeee c -i horario.csv', 'pending', '2018-05-23 15:58:22.548727', 'files/input/horario_uc1w0ZN.csv', '', 1, 6, 'Sma3s v2'),
(41, 'sma3s_v2.exe ssss a -t a eeeee c -i horario.csv', 'pending', '2018-05-23 16:00:07.431784', 'files/input/horario_FKq9oER.csv', '', 1, 6, 'Sma3s v2'),
(42, 'sma3s_v2.exe ssss a -t e eeeee c -i Cursos.csv', 'pending', '2018-05-23 16:00:32.913870', 'files/input/Cursos_wz4MOLP.csv', '', 1, 6, 'Sma3s v2'),
(43, 'sma3s_v2.exe ssss a -t ccccccc eeeee c -i InformeT035-Mayo.ods', 'pending', '2018-05-23 17:23:18.279284', 'files/input/InformeT035-Mayo.ods', '', 1, 6, 'Sma3s v2'),
(44, 'sma3s_v2.exe ssss a -t ccccccc eeeee c -i InformeT035-Mayo.ods', 'pending', '2018-05-23 17:27:54.582390', 'files/input/InformeT035-Mayo_JRabmQx.ods', '', 1, 6, 'Sma3s v2-daniel@gmail.com2018-05-23 17:28:11'),
(45, 'sma3s_v2.exe ssss a -t ccccssss eeeee c -i InformeT035-Mayo.ods', 'pending', '2018-05-23 17:31:07.248593', 'files/input/InformeT035-Mayo_Mftp2e0.ods', '', 1, 6, 'sma3sv2-daniel@gmail.com2018-05-23 17:31:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_group`:
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_group_permissions`:
--   `permission_id`
--       `auth_permission` -> `id`
--   `group_id`
--       `auth_group` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_permission`:
--   `content_type_id`
--       `django_content_type` -> `id`
--

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add permission', 3, 'add_permission'),
(8, 'Can change permission', 3, 'change_permission'),
(9, 'Can delete permission', 3, 'delete_permission'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add image slideshow', 7, 'add_imageslideshow'),
(20, 'Can change image slideshow', 7, 'change_imageslideshow'),
(21, 'Can delete image slideshow', 7, 'delete_imageslideshow'),
(22, 'Can add app', 8, 'add_app'),
(23, 'Can change app', 8, 'change_app'),
(24, 'Can delete app', 8, 'delete_app'),
(25, 'Can add section', 9, 'add_section'),
(26, 'Can change section', 9, 'change_section'),
(27, 'Can delete section', 9, 'delete_section'),
(28, 'Can add params input', 10, 'add_paramsinput'),
(29, 'Can change params input', 10, 'change_paramsinput'),
(30, 'Can delete params input', 10, 'delete_paramsinput'),
(31, 'Can add Profile', 11, 'add_profile'),
(32, 'Can change Profile', 11, 'change_profile'),
(33, 'Can delete Profile', 11, 'delete_profile'),
(34, 'Can add task', 12, 'add_task'),
(35, 'Can change task', 12, 'change_task'),
(36, 'Can delete task', 12, 'delete_task'),
(37, 'Can add my company', 13, 'add_mycompany'),
(38, 'Can change my company', 13, 'change_mycompany'),
(39, 'Can delete my company', 13, 'delete_mycompany'),
(40, 'Can add params input text', 14, 'add_paramsinputtext'),
(41, 'Can change params input text', 14, 'change_paramsinputtext'),
(42, 'Can delete params input text', 14, 'delete_paramsinputtext'),
(43, 'Can add params input select', 15, 'add_paramsinputselect'),
(44, 'Can change params input select', 15, 'change_paramsinputselect'),
(45, 'Can delete params input select', 15, 'delete_paramsinputselect'),
(46, 'Can add params input file', 16, 'add_paramsinputfile'),
(47, 'Can change params input file', 16, 'change_paramsinputfile'),
(48, 'Can delete params input file', 16, 'delete_paramsinputfile'),
(49, 'Can add param input option', 17, 'add_paraminputoption'),
(50, 'Can change param input option', 17, 'change_paraminputoption'),
(51, 'Can delete param input option', 17, 'delete_paraminputoption');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_user`:
--

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(4, 'pbkdf2_sha256$36000$lFWGiZW4EjEh$yilpdKdK351w3IOKh16ToFyWM2xm1r+6Fl2HMWWDHgk=', '2018-03-28 22:25:36.768328', 0, 'laura@gmail.com', 'Laura', 'Manrique Guisado', 'laura@gmail.com', 0, 1, '2018-03-28 22:23:36.181500'),
(6, 'pbkdf2_sha256$36000$vWRpawn5QjTj$wPCT+TgWokDFt2l+ujHeKBJ3aBrKHH5qQ1e0xeXSsPk=', '2018-06-06 09:30:49.222480', 1, 'daniel@gmail.com', 'Daniel', 'Exposito', 'daniel@gmail.com', 0, 1, '2018-05-05 08:45:23.698373'),
(9, 'pbkdf2_sha256$36000$Xx1Nt1BnuIhC$1nJLYPd4dG1QOOx1RIHb0du99iB5IkleOW1vlaY31d8=', NULL, 0, 'marcel@gmail.com', 'Marcel', 'Richter', 'marcel@gmail.com', 0, 1, '2018-05-05 11:24:34.953098');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_user_groups`:
--   `group_id`
--       `auth_group` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `auth_user_user_permissions`:
--   `permission_id`
--       `auth_permission` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `django_admin_log`:
--   `content_type_id`
--       `django_content_type` -> `id`
--   `user_id`
--       `auth_user` -> `id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `django_content_type`:
--

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(8, 'app', 'app'),
(7, 'app', 'imageslideshow'),
(13, 'app', 'mycompany'),
(17, 'app', 'paraminputoption'),
(10, 'app', 'paramsinput'),
(16, 'app', 'paramsinputfile'),
(15, 'app', 'paramsinputselect'),
(14, 'app', 'paramsinputtext'),
(11, 'app', 'profile'),
(9, 'app', 'section'),
(12, 'app', 'task'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `django_migrations`:
--

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2018-03-06 21:43:31.548643'),
(2, 'auth', '0001_initial', '2018-03-06 21:43:32.208151'),
(3, 'admin', '0001_initial', '2018-03-06 21:43:32.387692'),
(4, 'admin', '0002_logentry_remove_auto_add', '2018-03-06 21:43:32.425698'),
(5, 'app', '0001_initial', '2018-03-06 21:43:33.071746'),
(6, 'contenttypes', '0002_remove_content_type_name', '2018-03-06 21:43:33.225529'),
(7, 'auth', '0002_alter_permission_name_max_length', '2018-03-06 21:43:33.282904'),
(8, 'auth', '0003_alter_user_email_max_length', '2018-03-06 21:43:33.335175'),
(9, 'auth', '0004_alter_user_username_opts', '2018-03-06 21:43:33.348802'),
(10, 'auth', '0005_alter_user_last_login_null', '2018-03-06 21:43:33.391361'),
(11, 'auth', '0006_require_contenttypes_0002', '2018-03-06 21:43:33.395202'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2018-03-06 21:43:33.425565'),
(13, 'auth', '0008_alter_user_username_max_length', '2018-03-06 21:43:33.652683'),
(14, 'sessions', '0001_initial', '2018-03-06 21:43:33.725829'),
(15, 'app', '0002_auto_20180308_0626', '2018-03-08 06:26:36.820755'),
(16, 'app', '0003_auto_20180308_0634', '2018-03-08 06:34:19.516308'),
(17, 'app', '0004_remove_mycompany_images_slideshow', '2018-03-09 06:23:50.077575'),
(19, 'app', '0006_auto_20180317_1630', '2018-03-17 16:36:56.361995'),
(21, 'app', '0008_auto_20180317_1634', '2018-03-17 16:36:56.562309'),
(22, 'app', '0009_auto_20180317_1634', '2018-03-17 16:36:56.721861'),
(23, 'app', '0010_auto_20180317_1636', '2018-03-17 16:36:56.884370'),
(25, 'app', '0012_auto_20180317_1730', '2018-03-17 17:30:08.209980'),
(26, 'app', '0002_paramsinput_is_required', '2018-03-17 17:37:17.811153'),
(27, 'app', '0003_auto_20180317_1739', '2018-03-17 17:39:06.635932'),
(28, 'app', '0004_paramsinput_value', '2018-03-17 17:40:50.786804'),
(29, 'app', '0005_auto_20180317_1742', '2018-03-17 17:42:10.191247'),
(30, 'app', '0006_paramsinput_info', '2018-03-17 18:09:32.290074'),
(31, 'app', '0007_paramsinput_option', '2018-03-17 18:54:28.608713'),
(32, 'app', '0008_auto_20180325_1611', '2018-03-25 16:11:57.907458'),
(33, 'app', '0009_task_taskcode', '2018-03-25 16:51:20.318828'),
(34, 'app', '0010_auto_20180325_2222', '2018-03-25 22:22:07.578495'),
(35, 'app', '0011_auto_20180519_1702', '2018-05-19 17:02:22.759388'),
(36, 'app', '0012_auto_20180520_0904', '2018-05-20 09:04:45.378380'),
(37, 'app', '0013_auto_20180520_1712', '2018-05-20 17:12:43.022772');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- RELACIONES PARA LA TABLA `django_session`:
--

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('11h730jfb687porqr2xda24h9nbl56au', 'ZjRmZjZlNDMzNzk0MDE1ZjhjZjMxOGUyZGE1N2NkZGVhM2MwNGE5MDp7Il9hdXRoX3VzZXJfaGFzaCI6IjNiOGI1YjQzNjZmMWRmNTRmZmVlZTRlNzdkOTAzOTExNTljMjk0N2UiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=', '2018-06-20 09:30:49.227287'),
('3xvp07beiaehsaagsexzbwajy8y0mdr3', 'ZTRmNmQ1MWRkOWUyYzgyZWNlMWFlMzhkNjc4M2FiZDY3MDRlZDMzZDp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-05-14 15:36:01.413299'),
('67lazmya4wrp4y8x3q6xnqrali131rtr', 'ZWQ1NTI5OTk5NGZkYWE1ZTAyODJjM2MyOTI2OTEwZTYzNzU4YTExOTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-04-26 21:45:32.865708'),
('h7rp7u950ou7wu8ivfxawr606l218qkg', 'ZTRmNmQ1MWRkOWUyYzgyZWNlMWFlMzhkNjc4M2FiZDY3MDRlZDMzZDp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-03-28 22:48:11.093364'),
('kqzgz9dm3vvsrhri0w3evr9g11oo43k9', 'ZTRmNmQ1MWRkOWUyYzgyZWNlMWFlMzhkNjc4M2FiZDY3MDRlZDMzZDp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-05-12 15:03:47.311867'),
('la6gwbzlr2830nacbvjjcaktgwkrlgho', 'ZTRmNmQ1MWRkOWUyYzgyZWNlMWFlMzhkNjc4M2FiZDY3MDRlZDMzZDp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-03-28 22:11:28.315113'),
('nfqch0y0upa73cmylg10ksztok02zp75', 'ZTRmNmQ1MWRkOWUyYzgyZWNlMWFlMzhkNjc4M2FiZDY3MDRlZDMzZDp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg1NGViZDE4ZmY2ZDljZWEwOWUzMjJiOTE0MjAwYzQxZDU0NzkzNTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-04-11 22:29:08.426249');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `app_app`
--
ALTER TABLE `app_app`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_appcompatibility`
--
ALTER TABLE `app_appcompatibility`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_app_app_compatibility`
--
ALTER TABLE `app_app_app_compatibility`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_app_app_compatibility_from_app_id_to_app_id_0c35be2b_uniq` (`from_app_id`,`to_app_id`),
  ADD KEY `app_app_app_compatibility_to_app_id_063d3fad_fk_app_app_id` (`to_app_id`);

--
-- Indices de la tabla `app_imageslideshow`
--
ALTER TABLE `app_imageslideshow`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_mycompany`
--
ALTER TABLE `app_mycompany`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_paraminputoption`
--
ALTER TABLE `app_paraminputoption`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_paraminputoption_select_id_5bc6201f_fk_app_param` (`select_id`);

--
-- Indices de la tabla `app_paramsinput`
--
ALTER TABLE `app_paramsinput`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_paramsinput_app_id_1fb3d096_fk_app_app_id` (`app_id`);

--
-- Indices de la tabla `app_paramsinputfile`
--
ALTER TABLE `app_paramsinputfile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_paramsinputfile_app_id_80d96a6a_fk_app_app_id` (`app_id`);

--
-- Indices de la tabla `app_paramsinputselect`
--
ALTER TABLE `app_paramsinputselect`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_paramsinputselect_app_id_02e0212c_fk_app_app_id` (`app_id`);

--
-- Indices de la tabla `app_paramsinputtext`
--
ALTER TABLE `app_paramsinputtext`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_paramsinputtext_app_id_2ccb0b56_fk_app_app_id` (`app_id`);

--
-- Indices de la tabla `app_profile`
--
ALTER TABLE `app_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `app_section`
--
ALTER TABLE `app_section`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_section_subsection_id_01fbe031_fk_app_section_id` (`subsection_id`),
  ADD KEY `app_section_app_id_741dba7d_fk_app_app_id` (`app_id`);

--
-- Indices de la tabla `app_task`
--
ALTER TABLE `app_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_task_app_id_d3f90c3c_fk_app_app_id` (`app_id`),
  ADD KEY `app_task_user_id_1430ba9d_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `app_app`
--
ALTER TABLE `app_app`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `app_appcompatibility`
--
ALTER TABLE `app_appcompatibility`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `app_app_app_compatibility`
--
ALTER TABLE `app_app_app_compatibility`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `app_imageslideshow`
--
ALTER TABLE `app_imageslideshow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT de la tabla `app_mycompany`
--
ALTER TABLE `app_mycompany`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `app_paraminputoption`
--
ALTER TABLE `app_paraminputoption`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT de la tabla `app_paramsinput`
--
ALTER TABLE `app_paramsinput`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT de la tabla `app_paramsinputfile`
--
ALTER TABLE `app_paramsinputfile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT de la tabla `app_paramsinputselect`
--
ALTER TABLE `app_paramsinputselect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `app_paramsinputtext`
--
ALTER TABLE `app_paramsinputtext`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT de la tabla `app_profile`
--
ALTER TABLE `app_profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT de la tabla `app_section`
--
ALTER TABLE `app_section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `app_task`
--
ALTER TABLE `app_task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;
--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_app_app_compatibility`
--
ALTER TABLE `app_app_app_compatibility`
  ADD CONSTRAINT `app_app_app_compatibility_from_app_id_ee0af148_fk_app_app_id` FOREIGN KEY (`from_app_id`) REFERENCES `app_app` (`id`),
  ADD CONSTRAINT `app_app_app_compatibility_to_app_id_063d3fad_fk_app_app_id` FOREIGN KEY (`to_app_id`) REFERENCES `app_app` (`id`);

--
-- Filtros para la tabla `app_paraminputoption`
--
ALTER TABLE `app_paraminputoption`
  ADD CONSTRAINT `app_paraminputoption_select_id_5bc6201f_fk_app_param` FOREIGN KEY (`select_id`) REFERENCES `app_paramsinputselect` (`id`);

--
-- Filtros para la tabla `app_paramsinput`
--
ALTER TABLE `app_paramsinput`
  ADD CONSTRAINT `app_paramsinput_app_id_1fb3d096_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`);

--
-- Filtros para la tabla `app_paramsinputfile`
--
ALTER TABLE `app_paramsinputfile`
  ADD CONSTRAINT `app_paramsinputfile_app_id_80d96a6a_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`);

--
-- Filtros para la tabla `app_paramsinputselect`
--
ALTER TABLE `app_paramsinputselect`
  ADD CONSTRAINT `app_paramsinputselect_app_id_02e0212c_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`);

--
-- Filtros para la tabla `app_paramsinputtext`
--
ALTER TABLE `app_paramsinputtext`
  ADD CONSTRAINT `app_paramsinputtext_app_id_2ccb0b56_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`);

--
-- Filtros para la tabla `app_profile`
--
ALTER TABLE `app_profile`
  ADD CONSTRAINT `app_profile_user_id_87d292a0_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `app_section`
--
ALTER TABLE `app_section`
  ADD CONSTRAINT `app_section_app_id_741dba7d_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`),
  ADD CONSTRAINT `app_section_subsection_id_01fbe031_fk_app_section_id` FOREIGN KEY (`subsection_id`) REFERENCES `app_section` (`id`);

--
-- Filtros para la tabla `app_task`
--
ALTER TABLE `app_task`
  ADD CONSTRAINT `app_task_app_id_d3f90c3c_fk_app_app_id` FOREIGN KEY (`app_id`) REFERENCES `app_app` (`id`),
  ADD CONSTRAINT `app_task_user_id_1430ba9d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
