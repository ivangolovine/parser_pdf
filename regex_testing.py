import re



def testing_regex_input():
    list1 = ['6/11/23, 11:16 PM', 'Eureka', 'https://nouveau-eureka-cc.ezproxy.biblioottawalibrary.ca/Search/ResultMobile',
             '14/962', 'La Presse+', 'ACTUALITÉS, mercredi 13 novembre 2019 1077 mots, p. ACTUALITÉS_6', 'CHRONIQUE',
             'Violence généalogique et autres impostures', 'Isabelle Hachêy', 'La Presse',
             "Dire que tout ce temps-là, j'étais autochtone, et que personne n'avait cru bon m'en avertir. Quelle bande de petits cachottiers",
             'dans ma famille, quand même.', "C'est en lisant les journaux, la semaine dernière, que j'ai découvert le pot aux roses.", "C'est que, voyez-vous, l'ancêtre métis de Marie-Josée Parent, qui nous a été présentée lors de son élection, en 2017, comme",
             "la première conseillère autochtone de l'histoire de la Ville de Montréal, est aussi… le mien.", 'Cet ancêtre, Michel Haché dit Gallant (1663-1737), est en effet le patriarche de tous les Haché – et des noms dérivés',
             "Hachey, Hachez, Aché, etc. – d'Acadie.", "Or, la rumeur court au sujet du père Michel. À ce qu'on dit, son papa, venu tout droit de France, aurait épousé une « sauvage",
             '». Quoique… peut-être pas non plus.', 'Depuis longtemps, les origines de mon ancêtre divisent les généalogistes acadiens. « La question du sang amérindien de', "Michel Haché reste toujours aussi incertaine », lisait-on encore en 2016 dans L'Acadie Nouvelle.",
             "Mais qu'importe ! Cet ancêtre peut-être métis, peut-être pas, ayant vécu il y a trois siècles, a suffi à la conseillère de", 'Verdun, Marie-Josée Parent, pour se dire membre de la communauté micmaque.', "Jusqu'à la semaine dernière, elle était responsable du dossier de la réconciliation entre la Ville de Montréal et les peuples", 'autochtones.',
             "Avant d'être élue, elle a été coprésidente du Réseau pour la stratégie urbaine de la communauté autochtone de Montréal.", 'Elle a aussi été directrice générale de DestiNations, un organisme subventionné qui voulait établir une ambassade culturelle', 'autochtone à Montréal.', '***', 'Pendant des années, Marie-Josée Parent a roulé tout le monde dans la farine. Les médias, les autochtones, les',
             'gouvernements, ses collègues, la mairesse, les élus, ses électeurs.', "Soyons clairs : elle n'est pas plus autochtone que moi.", 'Soyons encore plus clairs : elle a menti en toute connaissance de cause sur ses origines.', "Elle s'est fait passer pour ce qu'elle n'est pas pour fonder et diriger un organisme « autochtone », puis pour être élue et pour",
             'décrocher un poste de responsabilité au sein du comité exécutif de la Ville.', "Rendu là, ce n'est plus que de l'appropriation culturelle ; c'est de l'usurpation d'identité. C'est de la supercherie.",
             "Et elle s'en tire avec une tape sur les doigts…", "Selon la version officielle, Marie-Josée Parent a elle-même décidé d'abandonner son poste à la réconciliation, la semaine",
             'dernière, quand ses origines autochtones ont été remises en doute par deux généalogistes.', 'Pour ne pas causer de distraction inutile, nous a-t-on expliqué.', 'La Presse (site web)',
             '13 novembre 2019', '-', 'Aussi paru dans']

    regex_name = "^[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-.]* +[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ][a-zA-ZÀ-Ÿ-. ]*"

    '''for name in list1:
        if re.match(regex_name, name) and "La Presse" not in name:
            print(name)'''
    index1 = 0
    extracted_name = list1[index1]
    print(len(list1))

    while index1 < len(list1):
        extracted_name = list1[index1]
        if "La Presse"  in extracted_name:
            index1 += 1
            continue

        if re.match(regex_name, extracted_name):
            print(index1)
            break
        index1 += 1

    print(extracted_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testing_regex_input()