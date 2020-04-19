CREATE TABLE `blog_posts` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`date_published` date NOT NULL,
	`title` varchar(300) NOT NULL,
	`link_name` varchar(300) NOT NULL,
	`author` varchar(100) NOT NULL,
	`img_id` int(11) DEFAULT NULL,
	`content` mediumtext NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `img_ids` (
	`id` int(11) unsigned NOT NULL,
	PRIMARY KEY (`id`)
);
