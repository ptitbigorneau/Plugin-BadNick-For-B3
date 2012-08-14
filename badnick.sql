-- phpMyAdmin SQL Dump
-- version 3.3.10deb1
-- http://www.phpmyadmin.net
--
-- Serveur: localhost
-- Généré le : Mer 03 Août 2011 à 10:52
-- Version du serveur: 5.1.54
-- Version de PHP: 5.3.5-1ubuntu7.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `b32`
--

-- --------------------------------------------------------

--
-- Structure de la table `badnick`
--

CREATE TABLE IF NOT EXISTS `badnick` (
  `nick` varchar(32) NOT NULL,
  `ban` varchar(32) NOT NULL,
  KEY `nick` (`nick`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `badnick`
--

