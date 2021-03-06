# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.0 - 2022-07-19
### Changed
* class constructors input optional attributes separately
* create timestamp by default if no (begin/end) timestamp is provided
  * rename flag add_time_stamp to add_timestamp
* validate layer name at linguistic processor or layer creation
* restrict target-id map creation

### Fixed
* add missing `Span` attribute to `Chunk` objects

## 0.2.1 - 2022-06-16
### Fixed
* Add missing implementations of `dates` and `locations` elements

## 0.2.0 - 2022-06-09
### Changed

* all classes with a `Span` attribute implement `IdrefGetter` and `target_ids()` function
* add `replace` flag to `add_linguistic_processor`, `add_lp` and `extend_lps` functions

### Fixed

* DTD validation 

## 0.1 - initial commit up to 2022-06-08
Everything from initial commit up to conforming to NAF 3.3.