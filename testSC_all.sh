for fich in testSC*.py
do
	echo -e "\n---------------"
	echo "$fich"
	echo "---------------"
	python3 $fich
	echo "--------------------------------------------"
	read -n1 -r -p "Appuyez sur une touche pour continuer..." key
done
